import csv
import io

from server.application.catalogs.views import CatalogExportView


def to_csv(export: CatalogExportView) -> str:
    fieldnames = [
        "titre",
        "description",
        "service",
        "couv_geo",
        "format",
        "si",
        "contact_service",
        "contact_personne",
        "freq_maj",
        "date_maj",
        "url",
        "licence",
        "mots_cles",
    ]

    fieldnames.extend(extra_field.name for extra_field in export.catalog.extra_fields)

    f = io.StringIO()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for dataset in export.datasets:
        row = {
            "titre": dataset.title,
            "description": dataset.description,
            "service": dataset.service,
            "couv_geo": dataset.geographical_coverage,
            "format": ", ".join(fmt.name for fmt in dataset.formats),
            "si": dataset.technical_source or "",
            "contact_service": dataset.producer_email or "",
            "contact_personne": ", ".join(dataset.contact_emails),
            "freq_maj": (
                freq.value if (freq := dataset.update_frequency) is not None else ""
            ),
            "date_maj": (
                d.strftime("%d/%m/%Y")
                if (d := dataset.last_updated_at) is not None
                else ""
            ),
            "url": dataset.url or "",
            "licence": dataset.license or "",
            "mots_cles": ", ".join(tag.name for tag in dataset.tags),
        }

        extra_field_value_by_id = {
            extra_field_value.extra_field_id: extra_field_value.value
            for extra_field_value in dataset.extra_field_values
        }

        for extra_field in export.catalog.extra_fields:
            row[extra_field.name] = extra_field_value_by_id.get(extra_field.id, "")

        writer.writerow(row)

    return f.getvalue()
