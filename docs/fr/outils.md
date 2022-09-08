# Outils de développement

## Migrations

Les migrations de la base de données sont gérées avec [`alembic`](https://alembic.sqlalchemy.org/en/latest/).

Pour appliquer les migrations en attente :

```bash
make migrate
```

Pour créer une nouvelle migration :

```bash
name=create-some-table make migration
```

Pour voir l'état actuel des migrations :

```bash
make currentmigration
```

## Données initiales

_Pour l'utilisation dans les environnements de déploiement, voir [Opérations - Données initiales](./ops.md#données-initiales)._

Le script `tools/initdata.py` permet de définir des données initiales à charger en base.

Il peut être lancé comme suit :

```
make initdata
```

Des entités seront ainsi chargées en base de données.

Si celles-ci ont changé (suite à des manipulations manuelles dans le frontend, par exemple) et que vous souhaitez les remettre dans leur état initial, lancer :

```
make initdatareset
```

Ces commandes `make` sont branchées sur le fichier `tools/initdata.yml`. Pour utiliser un fichier différent, invoquer le script Python directement :

```
venv/bin/python -m tools.initdata <file>
```

La structure d'un fichier d'initdata est ad-hoc, et fortement corrélée au traitement réalisé par le script.

Structure :

* `users` - list
  * `id` - str - UUID
  * `params` - dict
    * `email` - str
    * `password` - str - Utiliser `__env__` pour tirer le mot de passe de `TOOLS_PASSWORDS`
  * `extras` - _Optionnel_, dict
    * `role` - str, `USER | ADMIN`
* `tags` - list
  * `id` - str - UUID
  * `params` - dict
    * `name` - str
* `datasets` - list
  * `id` - str - UUID
  * `params` - dict
    * title, description, et autres champs de [`DatasetCreate` (API docs)](https://demo.catalogue.multi.coop/api/docs)

Il est possible de passer des mots de passe utilisateur secrets en utilisant la valeur spéciale `password: __env__`. Le mot de passe correspondant à l'email doit alors être défini dans un objet JSON via la variable d'environnement `TOOLS_PASSWORD` :

```bash
TOOLS_PASSWORDS='{"email1": "password1", "email2": "password2", ...}' venv/bin/python -m tools.initdata /path/to/initdata.yml
```

Exemple :

```yaml
users:
  - # Utilisateur standard.
    id: "<UUID>"
    params:
      email: "john.doe@example.org"
      password: "example"
  - # Utilisateur admin.
    # Mot de passe défini par $TOOLS_PASSWORDS, ou demandé en ligne de commande si vide.
    id: "<UUID>"
    params:
      email: "sarah.conor@example.org"
      password: __env__
    extras:
      role: ADMIN
  - # ...

tags:
  - id: "<UUID>"
    params:
      name: "<name>"
  - # ...

datasets:
  - id: "<UUID>"
    params:
      title: "<title>"
      description: "<description>"
      formats:
        - "<format>"
      # ...
  - # ...
```

Utilisation :

```
TOOLS_PASSWORDS='{"sarah.conor@example.org": "sarahpwd"}' venv/bin/python -m tools.initdata /path/to/initdata.yml
```

N.B. : Avant de créer chaque entité, le script s'assure qu'elle n'existe pas déjà en base. En passant le flag `--reset` (intégré dans `make initdatareset`), les champs des entités existantes sont réinitialisées à leurs valeurs définies dans le fichier YAML.

Pour plus de détails, lire le code source.

### Jeux de données aléatoires

Il est possible d'ajouter un paquet de jeux de données aléatoires au catalogue d'une organisation de cette façon:

```bash
siret=... make randomdatasets
```

Par défaut 500 jeux de données sont ajoutés. Pour en ajouter une autre quantité, utiliser :

```bash
siret=... n=... make randomdatasets
```

## Générer un UUID

Pour générer un UUID d'entité, lancer :

```
make id
```

Exemple de sortie :

```
9355b423-4417-4153-8fd6-524697f8c88f
```

## Diagramme de la base de données

Le fichier `docs/db.erd.json` permet de générer un diagramme du schéma de la base de données.

Pour cela, installer d'abord [`graphviz`](https://graphviz.org/download/) (sous Linux : `$ sudo apt install graphviz`).

Puis lancer :

```
make dbdiagram
```

Ce qui génèrera `docs/db.png`.

Le format de `docs/db.erd.json` reprend celui de [`erdot`](https://github.com/ehne/ERDot), dont la documentation peut donc vous être utile.

## mypy

Ce projet est équipé du _type checking_ avec [`mypy`](https://mypy.readthedocs.io).

La vérification se fait avec une exécution standard de `$ mypy` lors de `make check`.

## Tests

### Tests E2E

Les tests _end-to-end_ sont lancés avec [`Playwright`](https://playwright.dev/).
Il sont soit exécutés en mode _ci_ (continuous integration, par exemple dans
notre cas avec github actions), et donc en _headless_, soit de manière
interactive (en dev).

### Tests unitaires - Client

Les tests unitaires côté client utilisent [`svelte-testing-library`](https://github.com/testing-library/svelte-testing-library).

Autres ressources pour démarrer :

- [Svelte Testing Library: Example](https://testing-library.com/docs/svelte-testing-library/example)
- [Unit Testing Svelte Components](https://sveltesociety.dev/recipes/testing-and-debugging/unit-testing-svelte-component/)

#### Astuces

* Utiliser `cd client && npm run test:watch` pour lancer les tests en mode "watch" : les tests seront relancés automatiquement au fur et à mesure que vous modifiez le code. Très pratique pour itérer rapidement sur des tests unitaires.

## DSFR

Le site utilise le [Design System de
l'État](https://gouvfr.atlassian.net/wiki/spaces/DB/overview) (aussi appelé
*DSFR*).

Il existe aussi le site très pratique de [Démo du design système
de l'état](https://template.incubateur.net/) pour la mise en œuvre et
l'utilisation de ce DSFR.

### Icônes supplémentaires

Le DSFR tire ses [icônes](https://gouvfr.atlassian.net/wiki/spaces/DB/pages/222331396/Ic+nes+-+Icons) de RemixIcon, mais seule une partie est incluse (pour des raisons de poids).

Des icônes supplémentaires utilisées dans ce projet sont fournies par un fichier CSS `client/src/styles/dsfr-icon-extras.css`. Celui-ci est généré par le script `tools/iconextras.py`.

Pour ajouter de nouvelles icônes supplémentaires :

- Récupérer le SVG (24px) sur https://remixicon.com/
- Ajouter le fichier SVG au dossier `client/src/assets/icon/dsfr-icon-extras/`
  - **Important** : retirer toute éventuelle propriété `fill="none"`. Le SVG ne doit contenir que le tracé, de sorte à être librement manipulable par CSS.
- Lancer `$ make dsfr-icon-extras` pour synchroniser le CSS.
- Utiliser les icônes comme d'habitude, mais avec `fr-icon-x-<name>` (`x` pour "extra") au lieu de `fr-icon-<name>`.
