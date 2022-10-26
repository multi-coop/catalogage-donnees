from pathlib import Path
from textwrap import dedent

import pytest
import yaml

from server.application.catalogs.commands import CreateCatalog
from server.config.di import resolve
from server.domain.catalogs.entities import BoolExtraField
from server.seedwork.application.messages import MessageBus
from tools import import_catalog

from ..factories import CreateOrganizationFactory, CreateTagFactory


@pytest.mark.asyncio
async def test_import_catalog_example(tmp_path: Path) -> None:
    csv_path = tmp_path / "catalog.csv"
    example_config_path = Path() / "tools" / "import.config.example.yml"
    out_path = tmp_path / "initdata.yml"

    bus = resolve(MessageBus)

    # Simulate an existing organization and catalog
    siret = await bus.execute(
        CreateOrganizationFactory.build(name="Ministère 1", siret="11004601800013")
    )
    await bus.execute(
        CreateCatalog(
            organization_siret=siret,
            extra_fields=[
                BoolExtraField(
                    organization_siret=siret,
                    name="donnees_geoloc",
                    title="Données géolocalisées",
                    hint_text="Les données sont-elles géolocalisées ?",
                    data={"true_value": "Oui", "false_value": "Non"},
                )
            ],
        )
    )

    # Simulate a pre-existing tag.
    await bus.execute(CreateTagFactory.build(name="Tag 1"))

    csv_path.write_text(
        dedent(
            """\
            titre;description;mots_cles;nom_orga;siret_orga;id_alt_orga;service;si;contact_service;contact_personne;date_pub;date_maj;freq_maj;couv_geo;url;format;licence;donnees_geoloc
            Titre1;Description1;"Tag 1,Tag 2";Ministère 1;11004601800013;;Direction1;SI1;service@mydomain.org;contact@mydomain.org;;2022-10-06;annuelle;aquitaine;;geojson, xls, oracle et shp;etalab-2.0;oui
            Titre2;Description2;"Tag 1,Tag 3";Ministère 1;11004601800013;;Direction1;SI2;service@mydomain.org;contact@mydomain.org;;;Invalid;NSP;;Information manquante;etalab-2.0;oui
            """  # noqa
        )
    )

    config_path = tmp_path / "catalogue.csv"
    config_path.write_text(
        example_config_path.read_text().replace("REPLACE_ME", str(csv_path))
    )

    code = await import_catalog.main(config_path, out_path)
    assert code == 0

    with out_path.open() as f:
        initdata = yaml.safe_load(f)

    assert not initdata["organizations"]
    assert not initdata["catalogs"]
    assert not initdata["users"]
    assert [t["params"] for t in initdata["tags"]] == [
        # "Tag 1" already existed
        {"name": "Tag 2"},
        {"name": "Tag 3"},
    ]

    assert len(initdata["datasets"]) == 2

    assert all(d["params"]["organization_siret"] == siret for d in initdata["datasets"])

    d0 = initdata["datasets"][0]["params"]
    assert sorted(d0["formats"]) == ["database", "file_gis", "file_tabular"]
    assert d0["geographical_coverage"] == "aquitaine"
    assert d0["update_frequency"] == "yearly"
    assert "[[ Notes d'import automatique ]]" not in d0["description"]

    d1 = initdata["datasets"][1]["params"]
    assert d1["geographical_coverage"] == "(Information manquante)"
    assert d1["formats"] == ["other"]
    assert d1["update_frequency"] is None
    assert d1["url"] is None
    assert "[[ Notes d'import automatique ]]" in d1["description"]
    assert "Format : (Information manquante)" in d1["description"]
    assert "Fréquence de mise à jour (valeur originale) : Invalid" in d1["description"]
