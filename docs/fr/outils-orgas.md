# Outils de gestion des organisations et catalogues

## Dépôt de configuration

_Aussi appelé "repo de config"_

Lien GitHub : [etalab/catalogage-donnees-config](https://github.com/etalab/catalogage-donnees-config)

Ce dépôt sert à stocker les organisations enregistrées sur l'instance de production [catalogue.data.gouv.fr](https://catalogue.data.gouv.fr) ainsi que leur catalogue au format [TableSchema](https://specs.frictionlessdata.io/table-schema/).

Pour en savoir plus sur son utilisation, consulter le README du dépôt de configuration.

## Importer un catalogue

Un outil expérimental _[lire : testé sommairement, et à modifier ou adapter selon les besoins]_ est disponible pour importer un catalogue.

### Utilisation

L'organisation et le catalogue doivent avoir été créés au préalable.

1. Écrire un fichier de configuration pour l'import à partir de l'exemple [import.config.example.yml](https://github.com/etalab/catalogage-donnees/blob/master/tools/import.config.example.yml).

1. Générer un fichier d'initdata grâce à l'outil :

    ```bash
    python -m tools.import_catalog <CONFIG_PATH> <OUT_PATH>
    ```

    Où `<CONFIG_PATH>` est le chemin du fichier de configuration écrit à l'instant, et `<OUT_PATH>` un chemin de sortie pour le fichier d'initdata résultant.

1. Tester l'import en local :

    * Partir d'une base de données vierge. Par exemple :
    
        ```
        dropdb catalogage
        createdb catalogage
        make migrate
        ```

    * Importer les organisations et catalogues à partir du dépôt de configuration. Pour ce faire :
        * Dans le `.env`, définir :
            ```dotenv
            APP_CONFIG_REPO_API_KEY=abcd1234  # N'importe quelle valeur
            ```
        * Démarrer le serveur d'API local avec `make serve`.
        * Dans le `.env` du dépôt de configuration, définir :
            ```dotenv
            CATALOGAGE_API_URL=abcd1234  # La même valeur que côté catalogage-donnees
            ```
            Puis lancer `make upload`.

    * Lancer l'initdata :

        ```bash
        python -m tools.initdata <OUT_PATH>
        ```

    * Démarrer le serveur et vérifier que l'import s'est correctement déroulé.

1. Si et seulement si le comportement local est validé, procéder à l'import en production :

    * Remplacer temporairement (sans faire de commit) le fichier d'initdata de la prod `ops/ansible/prod/assets/initdata.yml` par le fichier d'initdata généré.
    * Lancer `make ops-initdata env=prod`.
    * Remettre le fichier d'initdata de la prod dans son état d'origine (le git diff doit être vierge).
    * Vérifier le comportement en production.

### Options notables

* _(Requis)_ `organization_siret` - `str`

    SIRET de l'organisation dont il faut peupler le catalogue.

* _(Requis)_ `input_file.path` - `str`

    Chemin vers le fichier CSV contenant le catalogue.
    
    Les colonnes du CSV doivent refléter le schéma du catalogue tel que défini dans le dépôt de configuration :

    * Champs du schéma communs (`titre`, `description`, etc) ;
    * Champs complémentaires.

    Les colonnes ne correspondant ni au schéma commun, ni aux champs complémentaires, doivent être supprimées du fichier CSV ou, à défaut, explicitement indiquées dans `ignore_fields` (voir ci-dessous). Toute incohérence avec les champs complémentaires du catalogue en base de données entraînera une erreur.

* `ignore_fields` - `List[str]`

    La liste des colonnes ne correspondant ni au schéma commun, ni aux champs complémentaires.
