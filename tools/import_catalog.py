import argparse
import asyncio
import csv
import datetime as dt
import io
import sys
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Set, TextIO

import yaml
from pydantic import BaseModel, Field

from server.application.catalogs.queries import GetCatalogBySiret
from server.application.catalogs.views import ExtraFieldView
from server.application.organizations.queries import GetOrganizationBySiret
from server.application.tags.queries import GetAllTags
from server.config.di import bootstrap, resolve
from server.domain.common.types import ID, id_factory
from server.domain.datasets.entities import UpdateFrequency
from server.domain.organizations.types import Siret
from server.seedwork.application.messages import MessageBus
from tools.initdata import InitData


class InputCsv(BaseModel):
    path: Path
    encoding: str = "utf-8"
    delimiter: str = ","
    na_values: Set[str] = Field(default_factory=set)


class FormatsConfig(BaseModel):
    map: Dict[str, str] = Field(default_factory=dict)
    list_map: Dict[str, List[str]] = Field(default_factory=dict)


class UpdateFrequencyConfig(BaseModel):
    map: Dict[str, str] = Field(default_factory=dict)


class LastUpdatedAtConfig(BaseModel):
    format: str = "%Y-%M-%d"


class Config(BaseModel):
    input_csv: InputCsv
    organization_siret: Siret
    ignore_fields: Set[str] = Field(default_factory=set)
    formats: FormatsConfig = Field(default_factory=FormatsConfig)
    update_frequency: UpdateFrequencyConfig = Field(
        default_factory=UpdateFrequencyConfig
    )
    last_updated_at: LastUpdatedAtConfig = Field(default_factory=LastUpdatedAtConfig)


def _map_geographical_coverage(value: Optional[str], config: Config) -> str:
    if not value or value in config.input_csv.na_values:
        return "(Information manquante)"  # Field is required

    return value


def _map_formats(
    value: Optional[str], import_notes: TextIO, config: Config
) -> List[str]:

    if not value:
        return []

    def _map_format(value: str) -> List[str]:

        dataformat = config.formats.map.get(value, value)

        try:
            return [dataformat]
        except ValueError:
            return [value]

    result = list(set(f for val in value.split(",") for f in _map_format(val.strip())))

    return result


def _map_contact_emails(value: Optional[str]) -> List[str]:
    if value is None:
        return []

    return [value.strip().replace("<", "").replace(">", "")]


def _map_update_frequency(
    value: Optional[str], import_notes: TextIO, config: Config
) -> Optional[str]:
    if not value or value in config.input_csv.na_values:
        return None

    value = config.update_frequency.map.get(value.lower(), value)

    try:
        update_frequency = UpdateFrequency(value)
    except ValueError:
        import_notes.write(f"Fréquence de mise à jour (valeur originale) : {value}\n")
        return None

    return update_frequency.value


def _map_last_updated_at(value: Optional[str], config: Config) -> Optional[dt.datetime]:
    if value is None:
        return None

    return dt.datetime.strptime(value, config.last_updated_at.format)


def _map_tag_ids(
    value: Optional[str],
    existing_tag_ids_by_name: Mapping[str, ID],
    tags_to_create: List[dict],
) -> List[str]:
    if not value:
        return []

    tag_ids = []

    # Split and normalize tag names. For example:
    # "périmètre délimité des abords (PDA), urbanisme; géolocalisation"
    #   -> {"périmètre délimité des abords (PDA)", "urbanisme", "géolocalisation"}
    cleaned_names = set(name.strip() for name in value.replace(";", ",").split(","))

    for name in cleaned_names:
        try:
            tag_id = existing_tag_ids_by_name[name]
        except KeyError:
            tag_id = id_factory()
            tag = {"id": str(tag_id), "params": {"name": name}}
            tags_to_create.append(tag)

        tag_ids.append(str(tag_id))

    return tag_ids


def _map_extra_field_values(
    row: dict, extra_fields: List[ExtraFieldView]
) -> List[dict]:
    return [
        {"extra_field_id": str(extra_field.id), "value": value}
        for extra_field in extra_fields
        if (value := row[extra_field.name])
    ]


def _maybe_append_import_notes(description: str, import_notes: str) -> str:
    s = io.StringIO()

    s.write(description)

    if import_notes:
        s.writelines(
            ["\n", "[[ Notes d'import automatique ]]", "\n", import_notes, "\n"]
        )

    return s.getvalue()


async def main(config_path: Path, out_path: Path) -> int:
    bus = resolve(MessageBus)

    with config_path.open() as f:
        config = Config(**yaml.safe_load(f))

    organization = await bus.execute(
        GetOrganizationBySiret(siret=config.organization_siret)
    )
    catalog = await bus.execute(GetCatalogBySiret(siret=organization.siret))
    expected_extra_fields = {field.name for field in catalog.extra_fields}

    tags = await bus.execute(GetAllTags())
    existing_tag_ids_by_name = {tag.name: tag.id for tag in tags}

    with config.input_csv.path.open(encoding=config.input_csv.encoding) as f:
        reader = csv.DictReader(f, delimiter=config.input_csv.delimiter)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    common_fields = {
        "titre",
        "description",
        "siret_orga",
        "nom_orga",
        "service",
        "couv_geo",
        "formats",
        "si",
        "contact_service",
        "contact_personne",
        "freq_maj",
        "date_maj",
        "url",
        "licence",
        "mots_cles",
    }

    actual_extra_fields = set(fieldnames) - common_fields - config.ignore_fields

    if actual_extra_fields != expected_extra_fields:
        raise ValueError(
            f"Extra fields don't match: "
            f"{expected_extra_fields=}, {actual_extra_fields=}"
        )

    tags_to_create: List[dict] = []
    datasets = []

    for k, row in enumerate(rows):
        if (siret_orga := row["siret_orga"]) != organization.siret:
            raise ValueError(
                f"at row {k}: {siret_orga=!r} does not match {organization.siret=!r}"
            )

        if "nom_orga" in row and (nom_orga := row["nom_orga"]) != organization.name:
            raise ValueError(
                f"at row {k}: {nom_orga=!r} does not match {organization.name=!r}"
            )

        import_notes = io.StringIO()

        params: dict = {}

        params["organization_siret"] = organization.siret
        params["title"] = row["titre"]
        params["description"] = row["description"]
        params["service"] = row["service"] or None
        params["geographical_coverage"] = _map_geographical_coverage(
            row["couv_geo"] or None, config
        )
        params["formats"] = _map_formats(row["formats"] or None, import_notes, config)
        params["technical_source"] = row["si"] or None
        params["producer_email"] = row["contact_service"] or None
        params["contact_emails"] = _map_contact_emails(row["contact_personne"] or None)
        params["update_frequency"] = _map_update_frequency(
            row["freq_maj"] or None, import_notes, config
        )
        params["last_updated_at"] = _map_last_updated_at(
            row["date_maj"] or None, config
        )
        params["url"] = row["url"] or None
        params["license"] = row["licence"] or None
        params["tag_ids"] = _map_tag_ids(
            row["mots_cles"] or None, existing_tag_ids_by_name, tags_to_create
        )

        params["extra_field_values"] = _map_extra_field_values(
            row, catalog.extra_fields
        )

        params["description"] = _maybe_append_import_notes(
            params["description"], import_notes.getvalue()
        )

        pk = id_factory()
        datasets.append({"id": str(pk), "params": params})

    initdata = InitData(
        organizations=[],
        catalogs=[],
        users=[],
        tags=tags_to_create,
        datasets=datasets,
        formats=[],
    ).dict()

    out_path.write_text(yaml.safe_dump(initdata))

    return 0


if __name__ == "__main__":
    bootstrap()

    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", type=Path)
    parser.add_argument("out_path", type=Path)

    args = parser.parse_args()

    code = asyncio.run(main(config_path=args.config_path, out_path=args.out_path))

    sys.exit(code)
