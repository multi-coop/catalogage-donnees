# Opérations

**Table des matières**

- [Généralités](#généralités)
- [Environnements](#environnements)
  - [Liste des environnements](#liste-des-environnements)
  - [Versions](#versions)
  - [Ajouter un nouvel environnement](#ajouter-un-nouvel-environnement)
  - [Secrets](#secrets)
  - [Démanteler un environnement](#démanteler-un-environnement)
- [Intégrations](#intégrations)
  - [Comptes DataPass](#comptes-datapass)
- [Comment déployer](#comment-déployer)
  - [Installation](#installation)
  - [Déployer un environnement](#déployer-un-environnement)
  - [Déployer sur staging](#déployer-sur-staging)
  - [(Avancé) Déployer une version quelconque](#avancé-déployer-une-version-quelconque)
- [Outils](#outils)
  - [Données initiales](#données-initiales)
  - [Tester sur une VM locale](#tester-sur-une-vm-locale)
- [Débogage](#débogage)

## Généralités

Le déploiement et la gestion des serveurs distants est réalisée à l'aide de [Ansible](https://docs.ansible.com/ansible/latest/user_guide/index.html).

L'architecture du service déployé est la suivante :

```
        ┌---------------------------------┐
WWW ------- nginx (:443) --- node (:3000) |
        |      |               |          |
        |      └--------- uvicorn (:3579) |
        └----------------------|----------┘
                               |
                         ┌ - - ┴ - - -┐
                           PostgreSQL 
                         └ - - - - - -┘
```

Description : un Nginx sert de frontale web, et transmet les requêtes à un serveur applicatif Uvicorn qui communique avec la base de données PostgreSQL (pour les requêtes d'API), ou à un serveur Node (pour les requêtes client).

Par ailleurs :

* Uvicorn et Node sont gérés par le _process manager_ `supervisor`, ce qui permet notamment d'assurer leur redémarrage en cas d'arrêt inopiné.
* Le lien entre Uvicorn et la base de données PostgreSQL est paramétrable (_database URL_). Cette dernier ne vit donc pas nécessairement sur la même machine que le serveur applicatif.
* Nginx fait la terminaison TLS avec des certificats gérés avec [Certbot](https://eff-certbot.readthedocs.io) (LetsEncrypt).

## Environnements

### Liste des environnements

Les différents déploiements sont organisés en _environnements_ (copies de l'infrastructure) :

| Nom     | Description | URL | À déployer depuis |
|---------|-------------|-----|-------------------|
| prod    | Environnement de production | https://catalogue.data.gouv.fr | `master` |

⚠️ Depuis juillet 2023, l'instance de production a été migrée sur l'infrastructure de la DINUM. Les instance de démo et de staging ont été fermées. Les environnements actuels, ainsi que leurs ressources et localisations, n'ont pas encore été documentés.


Voici, à date, une liste des ressources pour chaque environnement et leur localisation.

| Ressource | Environnements | Lieu | Contact |
|-----------|----------------|------|---------|
| Instance cloud (VM) | Tous | ? | ? |
| Instance PostgreSQL | Tous | ? | ? |
| Enregistrement DNS | Tous | ? | ? |
| URLs de callback OpenID Connect pour "Comptes DataPass" | Tous | Infrastructure BetaGouv | Contacter l'équipe "Compte DataPass" sur BetaGouv, ou ouvrir un billet sur [betagouv/api-auth](https://github.com/betagouv/api-auth) |

### Versions

Voici la version des logiciels nécessaires ou installés via Ansible dans les environnements.

| Logiciel | Version | Notes |
|----------|---------|-------|
| OS | debian/bullseye64 | À sélectionner lors de la configuration de la VM chez l'hébergeur cloud |
| PostgreSQL | 12 | |
| Python | 3.8.x | Installé sur les serveurs distants avec [pyenv](https://github.com/pyenv/pyenv). Paramétré par la variable `pyenv_python_version`. Python peut être mis à jour en la modifiant. Penser à retirer toute ancienne version après une telle opération. |
| Node | v16.x | Installé sur les serveurs distants avec [nvm](https://github.com/nvm-sh/nvm). Paramétré par la variable `nvm_node_version`. |

### Ajouter un nouvel environnement

Pour créer un nouvel environnement, munissez-vous tout d'abord des ressources informatiques décrites dans [Liste des environnements](#liste-des-environnements).

Créez ensuite le dossier de l'environnement dans `ops/ansible/environments/`, sur le modèle de ceux qui existent déjà.

Les fichiers suivants sont attendus :

- `hosts` : _inventory_ Ansible.
- `secrets` : fichier de variables secrètes - voir [Secrets](#secrets) pour comment le modifier.
- `group_vars/web.yml` : variables spécifiques à l'environnement.

Quand tout semble prêt, initialisez l'environnement `<ENV>` :

```
make ops-provision env=<ENV>
```

Vous pouvez ensuite [déployer](#déployer-un-environnement).

### Secrets

La gestion des secrets s'appuie sur [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html).

Pour modifier le fichier de secrets d'un environnement, lancez :

```
make ops-secrets env=<ENV>
```

Voici quelques indications pour remplir ce fichier :

* `host` - IP de la VM.
* `secret_key` - Clé secrète de chiffrement des cookies.

    À générer avec : `$ make secretkey`

* `database_url` - URL de la base de données.

    **Important** : la portion mot de passe de l'URL doit être URL-encodée :

    ```python
    >>> from urllib.parse import quote_plus
    >>> quote_plus('mdp!des?caractèressp&ciaux')
    'mdp%21des%3Fcaract%C3%A8ressp%26ciaux'
    ```

* `config_repo_api_key` - Clé d'API du dépôt de configuration

    À générer avec : `$ make apikey`

* `datapass_client_id` - _Client ID_ de l'instance auprès du serveur OpenID Connect de Compte DataPass.
* `datapass_client_secret` - _Client secret_ de l'instance auprès du serveur OpenID Connect de Compte DataPass.

Astuce : vous pouvez aussi [chiffrer un fichier quelconque avec Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html#encrypting-files-with-ansible-vault) :

```
venv/bin/ansible-vault encrypt <FILE> --vault-password-file ops/ansible/vault-password
```

Pour modifier un fichier chiffré, utilisez :

```
venv/bin/ansible-vault edit <FILE> --vault-password-file ops/ansible/vault-password
```

### Démanteler un environnement

Un environnement peut devenir obsolète, par exemple parce qu'il n'est plus utile, qu'il a été remplacé par un autre environnement, ou tout autre cas faisant que l'instance associée doit être arrêtée.

Il s'agit alors de :

* S'assurer que l'environnement n'est plus utilisé et qu'il peut être supprimé définitivement.
* Ouvrir, passer en revue et merger une PR incluant les modifications suivantes :
  * Retirer le dossier de l'environnement de `ops/ansible`.
  * Retirer l'environnement de la présente documentation.
* Retirer les ressources informatiques allouées à cet environnement (voir [Liste des environnements](#liste-des-environnements)).

## Intégrations

### Comptes DataPass

L'outil délègue la gestion des organisations à [Comptes DataPass](https://github.com/betagouv/api-auth), un fédérateur d'entités de personnes morales.

La documentation de son serveur OpenID Connect est accessible dans leur [README](https://github.com/betagouv/api-auth/blob/1145f9edca8f4c4054922c7bebc98021c4858d80/README.md).

Dans les [secrets](#secrets) de chaque environnement est configuré un couple d'identifiants client ID/client correspondant à une instance Comptes DataPass, selon le tableau suivant :

| Environnement | Instance Comptes DataPass |
|---------------|---------------------------|
| prod          | production                |
| staging       | staging                   |
| demo          | staging                   |

En local, il est possible de copier les identifiants `staging` (depuis les secrets de l'environnement) dans son `.env` (voir [Configuration (Démarrage)](./demarrage.md#configuration)) pour développer avec l'authentification par DataPass.

## Comment déployer

### Installation

**Prérequis** :

- Accès en SSH aux instances cloud (demander à un membre de l'équipe).
- Mot de passe de déploiement (demander à un membre de l'équipe qui vous l'enverra de façon sécurisée).

Installez les dépendances supplémentaires pour interagir avec les outils d'infrastructure :

```
make ops-install
```

Placez le mot de passe de déploiement dans :

```
ops/ansible/vault-password
```

> Ce fichier est ignoré par git.

Vérifiez ensuite votre configuration avec :

```
cd ops && make ping env=staging
```

Vous devriez recevoir un "pong".

### Déployer un environnement

Pour déployer l'environnement `<ENV>`, lancez :

```
make ops-deploy env=<ENV>
```

En cas de problème, voir [Débogage](#débogage).

#### Déployer sur staging

L'environnement staging déploie la branche `staging`. Cette branche d'environnement a pour objet d'accueillir des changements de _pull requests_ afin de les valider et/ou prévisualiser.

Pour déployer les changements d'une _pull request_, il faut donc d'abord les ajouter à `staging`.

Pour cela :

1. Placez-vous sur la branche cible, par exemple :

    ```
    git checkout my-pr-branch
    ```

2. Ajoutez vos changements sur la branche staging en lançant :

    ```
    make ops-staging
    ```

> **Important** : les commits d'une PR ajoutés à staging ne doivent plus être modifiés. Autrement dit, le travail sur la PR doit continuer en ajoutant de nouveaux commits. Cela implique de ne plus faire de _rebase_ (pour récupérer des changements de `master`, par exemple) ni de _commit --amend_ sur les commits déjà synchronisés. En effet, la synchronisation avec staging se fait par _fast-forward merge_, qui échouera si les commits sont réécrits.

Vous devez ensuite déployer staging :

```
make ops-deploy env=staging
```

**N.B.** Tous les changements finalement adoptés dans `master` ne seront pas ajoutés à `staging`. La branche de staging devrait donc être régulièrement recréée à partir `master`. Pour vous y aider, lancez :

```
make ops-staging-sync
```

### (Avancé) Déployer une version quelconque

Si vous avez besoin de déployer une branche ou un commit particulier, par exemple pour rétablir une version particulière, lancez :

```
make ops-deploy env=<ENV> extra_opts="-e git_version=<GIT_VERSION>"
```

où `<GIT_VERSION>` peut être n'importe quelle [référence git](https://git-scm.com/book/fr/v2/Les-tripes-de-Git-R%C3%A9f%C3%A9rences-Git) : branche, tag, ou commit hash.

## Outils

### Données initiales

[L'outil de données initiales](./outils.md#données-initiales) peut être utilisé pour déployer des données initiales dans chaque environnement.

Pour cela :

- Ajouter un fichier d'initdata dans l'environnement, par exemple dans `ops/ansible/environments/<ENV>/assets/initdata.yml`
- _(Optionnel)_ Si le contenu de l'initdata est sensible, chiffrer le fichier (voir [Secrets](#secrets)).
- Ajouter une variable `initdata_src` dans `ops/ansible/environments/<ENV>/group_vars/web.yml` qui pointe vers le fichier d'initdata. Pour l'exemple ci-dessus, il conviendrait d'utiliser :

    ```yaml
    initdata_src: "{{ inventory_dir }}/assets/initdata.yml"
    ```

Vous pouvez alors lancer un initdata avec :

```
make ops-initdata env=<ENV>
```

### Tester sur une VM locale

Il est possible de tester la configuration Ansible sur une VM locale.

Vous pouvez par exemple configurer une box [Vagrant](https://www.vagrantup.com/docs/installation) comme suit :

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Configure VM
  config.vm.box = "debian/bullseye64"
  config.vm.network "private_network", ip: "192.168.56.10"
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 1
  end

  # Share host SSH public key with VM, so Ansible can execute commands over SSH.
  config.ssh.insert_key = false
  config.vm.provision "shell" do |s|
    ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
    s.inline = <<-SHELL
    echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
    echo #{ssh_pub_key} >> /root/.ssh/authorized_keys
    SHELL
  end
end
```

Démarrez la VM :

```bash
vagrant up
```

Accédez-y en SSH, en transmettant le port où se trouve votre base de données (BDD) de développement (ici 5432 sur l'hôte est transmis vers 5432 dans l'invité) ainsi que le port du serveur Nginx (ici 80 dans l'invité est transmis sur 3080 sur l'hôte) ([crédit pour cette astuce](https://stackoverflow.com/a/28506841)) :

```bash
vagrant ssh -- -R 5432:localhost:5432 -L 3080:localhost:80
```

Sur l'hôte, [ajoutez un environnement](#ajouter-un-nouvel-environnement) nommé `test` :

- `hosts` :

    ```
    [web]
    web-test ansible_host=192.168.56.10 ansible_user=vagrant
    ```

- `secrets` :
    ```yaml
    {}  # Rien de secret
    ```

- `group_vars/web.yml` :

    _(Modifiez `database_url` au besoin)_

    ```yaml
    git_version: master
    database_url: database_url: postgresql+asyncpg://user:pass@localhost:5432/catalogage
    ```

Vérifiez la bonne configuration avec un `ping` :

```
cd ops
make ping env=test
```

```
web-test | SUCCESS => { ... }
```

Lancez le _provisioning_ :

```
make ops-provision env=test
```

Vérifier la bonne exécution en inspectant dans la VM les différents outils et services attendus :

```console
$ pyenv --version
pyenv 2.2.3
```

```console
$ python -V
Python 3.8.9
```

```console
$ nvm --version
0.39.1
```

```console
$ node -v
v16.13.2
```

```console
$ systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy serv>
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor >
     Active: active (running) since Wed 2022-01-26 10:48:11 UTC; 48s ago
...
```

```console
$ systemctl status supervisor
● supervisor.service - Supervisor process control system for UNIX
     Loaded: loaded (/lib/systemd/system/supervisor.service; enabled; ve>
     Active: active (running) since Wed 2022-01-26 10:48:15 UTC; 59s ago
...
```

Puis déployez :

```
make ops-deploy env=test
```

Vérifiez le bon déploiement en accédant au site sur http://localhost:3080.

## Débogage

### Les migrations ont échoué

Pour l'instant, les déploiements ne sont pas _atomiques_. Si les migrations échouent, les fichiers de code auront déjà été mis à jour. Si un _reload_ de l'application survient (par Supervisor), le nouveau code sera pris en compte et il y a risque de plantage (désynchronisation entre le schéma de BDD attendu par le code et le schéma réel).

Il faut donc corriger les migrations, puis redéployer.

Une bonne pratique pour limiter les risques : déployer la migration d'abord, puis déployer le changement de code, avec éventuellement une migration de finalisation (ex : application de contraintes NULL), _c.f._ : https://gist.github.com/majackson/493c3d6d4476914ca9da63f84247407b

### Nginx renvoie une "502 Bad Gateway"

Il y a probablement soit un problème de configuration de la connexion entre Nginx et Node / Uvicorn (ex : mauvais port), soit le serveur Node / Uvicorn n'est pas _up_ (ex : il crashe ou ne démarre pas pour une raison à déterminer).

* Vérifier l'état de Nginx :

```
~/catalogage $ systemctl status nginx
```

* Vérifier l'état de Supervisor :

```
~/catalogage $ systemctl status supervisor
```

* Vérifier l'état du processus serveur (`server` pour Uvicorn, `client` pour le frontend Node) au sein de Supervisor :

```
~/catalogage $ sudo supervisorctl status server
```

* Inspecter la version du code, par exemple en inspectant le dépôt git :

```
~/catalogage $ git log
```

### Nginx ne redémarre pas

Il est probable que la configuration Nginx soit corrompue (ex: : accès à une ressource qui n'existe pas ou plus), y compris en raison d'une faiblesse dans le setup Ansible.

* Inspecter les logs d'erreurs / avertissements de Nginx :

```
~/catalogage $ nginx -t
```

### Certificats

**_(Avancé)_**

Les certificats TLS sont stockés par Certbot dans `/etc/letsencrypt` sur l'instance de chaque environnement.

Pour vérifier le cronjob de renouvellement des certificats :

```
crontab -l
```

Le résultat doit contenir :

```
#Ansible: certs_renewal
@weekly certbot renew -q
```

Pour lister les certificats, se connecter en SSH puis lancer :

```
$ certbot certificates
root@catalogage-dev:~# certbot certificates
Saving debug log to /var/log/letsencrypt/letsencrypt.log

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Found the following certs:
  Certificate Name: staging.catalogue.multi.coop
    Serial Number: 44fdad5f55bedd1be22e249bc9928b1977f
    Key Type: RSA
    Domains: staging.catalogue.multi.coop
    Expiry Date: 2022-06-26 14:59:19+00:00 (VALID: 89 days)
    Certificate Path: /etc/letsencrypt/live/staging.catalogue.multi.coop/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/staging.catalogue.multi.coop/privkey.pem
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

Pour régénérer manuellement les certificats pour un environnement :

1. Se connecter en SSH.
2. Révoquer le certificat :

    ```
    certbot revoke --cert-name <env>.catalogue.multi.coop
    ```

3. Redéployer : un nouveau certificat sera créé et configuré.

> N.B. : LetsEncrypt applique du _rate limiting_ à la délivrance de certificats. Voir [Let's Encrypt: Rate Limits](https://letsencrypt.org/docs/rate-limits/).
