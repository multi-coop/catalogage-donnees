from typing import Union

from sqlalchemy import and_, desc, func, or_, select, text
from sqlalchemy.engine import Row
from sqlalchemy.orm import contains_eager, selectinload

from server.domain.auth.entities import Account
from server.domain.common.types import Skip
from server.domain.datasets.entities import PublicationRestriction
from server.domain.datasets.repositories import DatasetGetAllExtras
from server.domain.datasets.specifications import DatasetSpec
from server.infrastructure.extra_fields.models import ExtraFieldValueModel

from ...catalog_records.models import CatalogRecordModel
from ...catalogs.models import CatalogModel
from ...tags.models import TagModel
from ..models import DataFormatModel, DatasetModel

_TS_HEADLINE_TITLE_COL = "ts_headline_title"
_TS_HEADLINE_DESCRIPTION_COL = "ts_headline_description"


class GetAllQuery:
    def __init__(self, spec: DatasetSpec, account: Union[Account, Skip]) -> None:
        columns = []
        joinclauses = []
        whereclauses = []
        orderbyclauses = []

        if (search_term := spec.search_term) is not None:
            # Search using a PostgreSQL text search vector (TSV).
            # See: https://www.postgresql.org/docs/12/textsearch-controls.html

            # Convert search term to normalized text search query.
            # E.g. 'Forêts françaises' -> 'forêt' & 'français'
            ts_query = func.plainto_tsquery(text("'french'"), search_term)

            # Compute search rank for each row
            # https://www.postgresql.org/docs/12/textsearch-controls.html#TEXTSEARCH-RANKING
            columns.append(
                func.ts_rank_cd(DatasetModel.search_tsv, ts_query).label("rank")
            )

            # Compute headlines (highlight markers) for title and description.
            # https://www.postgresql.org/docs/12/textsearch-controls.html#TEXTSEARCH-HEADLINE
            columns.append(
                func.ts_headline(
                    text("'french'"),
                    DatasetModel.title,
                    ts_query,
                    text("'StartSel=<mark>, StopSel=</mark>, HighlightAll=1'"),
                ).label(_TS_HEADLINE_TITLE_COL)
            )
            columns.append(
                func.ts_headline(
                    text("'french'"),
                    DatasetModel.description,
                    ts_query,
                    text("'StartSel=<mark>, StopSel=</mark>, MaxFragments=10'"),
                ).label(_TS_HEADLINE_DESCRIPTION_COL)
            )

            # Drop rows that don't match the search query.
            whereclauses.append(DatasetModel.search_tsv.op("@@")(ts_query))

            # Sort rows by search rank, best match first.
            orderbyclauses.append(desc(text("rank")))

        if isinstance(account, Skip):
            if organization_siret := spec.organization_siret:
                whereclauses.append(
                    and_(
                        CatalogRecordModel.organization_siret == organization_siret,
                    )
                )

            if not spec.include_all_datasets:
                whereclauses.append(
                    DatasetModel.publication_restriction
                    == PublicationRestriction.NO_RESTRICTION,
                )

        if isinstance(account, Account):
            if spec.organization_siret is not None:
                if spec.organization_siret == account.organization_siret:
                    whereclauses.append(
                        CatalogRecordModel.organization_siret
                        == spec.organization_siret,
                    )

                else:
                    whereclauses.append(
                        and_(
                            CatalogRecordModel.organization_siret
                            == spec.organization_siret,
                            DatasetModel.publication_restriction
                            == PublicationRestriction.NO_RESTRICTION,
                        )
                    )
            else:
                whereclauses.append(
                    or_(
                        CatalogRecordModel.organization_siret
                        == account.organization_siret,
                        DatasetModel.publication_restriction
                        == PublicationRestriction.NO_RESTRICTION,
                    )
                )

        if (geographical_coverages := spec.geographical_coverage__in) is not None:
            whereclauses.append(
                DatasetModel.geographical_coverage.in_(geographical_coverages),
            )

        if (services := spec.service__in) is not None:
            whereclauses.append(DatasetModel.service.in_(services))

        if (format_ids := spec.format__id__in) is not None:
            joinclauses.append((DatasetModel.formats, {"isouter": True}))
            whereclauses.append(DataFormatModel.id.in_(format_ids))

        if (technical_sources := spec.technical_source__in) is not None:
            whereclauses.append(DatasetModel.technical_source.in_(technical_sources))

        if (tag_ids := spec.tag__id__in) is not None:
            joinclauses.append((DatasetModel.tags, {"isouter": True}))
            whereclauses.append(TagModel.id.in_(tag_ids))

        if (license := spec.license) is not None:
            if license == "*":
                whereclauses.append(DatasetModel.license.is_not(None))
            else:
                whereclauses.append(DatasetModel.license == license)

        if (extra_field_value := spec.extra_field_value) is not None:
            joinclauses.append((DatasetModel.extra_field_values, {"isouter": True}))
            whereclauses.append(
                ExtraFieldValueModel.value.like(f"%{extra_field_value.value}%")
            )

        stmt = (
            select(DatasetModel, *columns)
            .join(DatasetModel.catalog_record)
            .join(CatalogRecordModel.catalog)
            .join(CatalogModel.organization)
        )

        for target, kwargs in joinclauses:
            stmt = stmt.join(target, **kwargs)

        self.statement = (
            stmt.options(
                contains_eager(DatasetModel.catalog_record)
                .contains_eager(CatalogRecordModel.catalog)
                .contains_eager(CatalogModel.organization),
                selectinload(DatasetModel.formats),
                selectinload(DatasetModel.tags),
                selectinload(DatasetModel.extra_field_values),
            )
            .where(*whereclauses)
            .order_by(*orderbyclauses, CatalogRecordModel.created_at.desc())
        )

    def instance(self, row: Row) -> DatasetModel:
        return row[0]

    def extras(self, row: Row) -> DatasetGetAllExtras:
        try:
            h_title = getattr(row, _TS_HEADLINE_TITLE_COL)
            h_description = getattr(row, _TS_HEADLINE_DESCRIPTION_COL)
        except AttributeError:
            return {}

        return {
            "headlines": {
                "title": h_title,
                "description": h_description if "<mark>" in h_description else None,
            }
        }
