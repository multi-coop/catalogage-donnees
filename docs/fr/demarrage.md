# Démarrage rapide

Cette page indique les quelques étapes qui vous permettront d'avoir un projet fonctionnel à partir duquel travailler.

* 👉 Je suis une personne non-technique et je souhaite rapidement lancer le projet : jetez un oeil à [Usage Docker](#usage-docker)
* 👉 Je suis une personne technique et je souhaite participer au développement détaillé : suivez le guide !

**Table des matières**

* [Usage Docker](#usage-docker)
* [Prérequis](#pr%C3%A9requis)
* [Interagir avec le projet](#interagir-avec-le-projet)
* [Configuration](#configuration)

---

## Usage Docker

Pour faciliter un démarrage rapide du projet, une configuration `docker-compose` est disponible, comprenant le serveur, le client, et une base de données.

Installez d'abord les outils nécessaires :

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (Testé avec la version `1.29` )

Puis lancez :

```
make compose-up
```

(Un mot de passe vous sera demandé la première fois pour la création du compte d'administration.)

Le client (application web) sera alors disponible sur http://localhost:3000.

Le client se rechargera automatiquement après des modifications dans le dossier `client/src/`, ce qui vous permettra d'y faire des modifications et de voir rapidement le résultat.

Pour toute autre modification, il faudra relancer Docker Compose : `make compose-down` puis `make compose-up`.

Pour arrêter le Docker Compose :

```
make compose-down
```

### Résolution de problème lors de l'installation

#### la commande `make compose-up` échoue

Dans ce cas ci, il est fort probable que la version de docker-compose ne soit plus à jour.

Vous pouvez les mettre à jour en suivant les instructions [ici](https://docs.docker.com/compose/install/#upgradinggit)

---

## Prérequis

Selon que vous vouliez contribuer au serveur ou au client, vous allez avoir besoin de :

### Pour le serveur

- Python 3.8+
- PostgreSQL 12

### Pour le client

- Une version récente de node (testé avec 16.3.0)
- Une version récente de npm (testé avec 8.1.3)

## Base de données

Il vous faut d'abord configurer une base de données PostgreSQL pour le développement.

Si vous avez un [serveur PostgreSQL](https://www.postgresql.org/download/linux/) sur votre machine hôte, lancez :

```bash
createdb catalogage
```

Sinon, vous pouvez utiliser la configuration `docker-compose` (voir [Usage Docker](#usage-docker)) :

```bash
docker-compose up -d -- db
```

[Configurez](#configuration) ensuite votre `APP_DATABASE_URL` :

```
cp .env.example .env
```

```bash
# .env
APP_DATABASE_URL="postgresql+asyncpg://user:pass@localhost:<PORT>/${DB:-catalogage}"
```

:warning: Remplacer `<PORT>` par la valeur du Port qui sera utilisé par la DB.

- Si vous disposez d'un serveur Postgres sur votre machine hôte le port sera `5432`
- Si vous utilisez Postgres via la configiguration du `docker-compose` alors le port sera `6432`

## Interagir avec le projet

La façon principale d'interagir avec le projet est via des commandes `make`. Elles sont définies dans le `Makefile`.

Vous pouvez à tout moment en consulter l'aide grace à `make help`.

Pour la plupart des commandes, il y a une déclinaison pour le serveur et pour le client.
Par exemple : `make install` est l'équivalent de `make install-server install-client`.
Vous pouvez ainsi soit installer toutes les dépendances pour le serveur ainsi que pour le client,
soit spécifier explicitement ce qui vous intéresse.

Voici la suite de commandes à exécuter pour démarrer.

Installez les dépendances :

```
make install
```

Ensuite, exécutez les migrations de la base de données :

```
make migrate
```

Puis remplissez le système avec quelques données initiales :

```
make initdata
```

Démarrez le serveur d'API (_backend_) sur http://localhost:3579 :

```
make serve-server
```

Démarrez le client (_frontend_) sur http://localhost:3000 :

```
make serve-client
```

Pour lancer les deux en parallèle dans le même shell :

```
make serve
```

Pour lancer l'ensemble des tests unitaires sur le client et le serveur, ainsi que les tests end-to-end (nécessite un `make serve` au préalable pour que les tests end-to-end fonctionnent) :

```
make test
```

Pour formatter le code automatiquement :

```
make format
```

Pour lancer les vérifications de qualité du code (_code linting_) :

```
make check
```

## Configuration

Le projet est configurable à l'aide des variables d'environnement suivantes.

| Variable | Description | Valeur par défaut |
|---|---|---|
| `APP_SECRET_KEY` | Clé secrète utilisée pour la signature des cookies | _Requis_ (Indice : en générer une avec [django-secret-key-generator](https://django-secret-key-generator.netlify.app/)) |
| `APP_DATABASE_URL` | URL vers la base de données PostgreSQL | `postgresql+asyncpg://localhost:5432/catalogage` |
| `APP_DATAPASS_CLIENT_ID` | `client_id` du serveur OpenID Connect de Comptes DataPass | - |
| `APP_DATAPASS_CLIENT_SECRET` | `client_secret` du serveur OpenID Connect de Comptes DataPass | - |
| `APP_DEBUG` | Active le mode debug : _debug logs_ SQL, [_debug toolbar_](https://github.com/mongkok/fastapi-debug-toolbar) dans la doc d'API | `False` |

Définissez les valeurs spécifiques à votre situation dans un fichier `.env` placé à la racine du projet, que vous pouvez créer à partir du modèle `.env.example` :

```
cp .env .env.example
```

Les variables peuvent aussi être passées en arguments, elles sont alors utilisées en priorité par rapport au `.env`.

Par exemple :

```bash
APP_DEBUG=1 make serve
```

En développement local, les variables `APP_DATAPASS_CLIENT_ID` et `APP_DATAPASS_CLIENT_SECRET` peuvent être configurées selon les identifiants de l'instance `staging` de Comptes DataPass. Voir [Comptes DataPass (Opérations)](./ops.md#comptes-datapass) pour plus d'informations.

Des paramètres avancés (principalement dédiés au déploiement - voir [Opérations](./ops.md)) sont également disponibles :

| Variable | Description | Valeur par défaut |
|---|---|---|
| `APP_SERVER_MODE` | Un mode d'opération qui configure Uvicorn en conséquence : <br> - `local` : pour le développement local (_hot reload_ activé, etc) <br> - `live` : pour tout déploiement tel que défini via Ansible | `local` |
| `APP_PORT` | Port du server d'API | `3579` |
| `APP_CONFIG_API_KEY` | Clé d'API pour le dépôt de configuration de l'instance | |
| `APP_CLIENT_URL` | URL du client, que le serveur d'API peut par exemple utiliser pour des besoins de redirection | `http://localhost:3000` |
| `TOOLS_PASSWORDS` | Mapping `email -> password`, voir [Données initiales](./outils.md#données-initiales)) | |
| `VITE_API_BROWSER_URL` | URL utilisée par le navigateur lors de requêtes d'API. En mode `live`, indiquer le chemin vers l'API configuré sur Nginx : `/api`. | `http://localhost:3579` |
| `VITE_API_SSR_URL` | URL utilisée par le serveur frontend lors de requêtes d'API | `http://localhost:3579` |
