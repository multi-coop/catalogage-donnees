# Architecture

## Généralités

Ce projet contient le _backend_ du logiciel libre de catalogage de données. Son rôle est donc d'exposer une API qui sera consommée par le _frontend_ ou des services tiers. Des objectifs de **maintenabilité long-terme** du projet ont été identifiés.

Dans ce contexte, l'architecture de code générale est inspirée des différentes approches suivantes, dans une variante adaptée au langage Python :

* [Domain-Driven Design](https://en.wikipedia.org/wiki/Domain-driven_design) (DDD)
* [Architecture hexagonale][0]

Ce choix architectural a été motivé par :

1. Le gain de maintenabilité long-terme observé sur les autres projets développés par [Fairness](https://fairness.coop) (dont le contributeur principal initial de ce projet est membre), dû notamment à un haut degré de découplage entre les couches métier, applicatives et techniques.
2. Un objectif de standardisation du projet (fichiers, concepts, processus), facilitant la navigation par toutes et tous, même si le projet grossit en taille et en complexité.

L'implémentation se veut légère et pragmatique. L'objectif premier est bien d'améliorer la maintenabilité, tout en évitant toute "cérémonie" excessive (_boilerplate_ réduit au maximum). Les contributeurs et contributrices ayant plutôt l'habitude de développer à même un framework (Django, FastAPI...) remarqueront que ce style architectural, de par le découplage qu'il permet, nécessite un peu plus de code (nombre de fichiers, lignes de code), et une gymnastique intellectuelle un peu différente. Mais la récompense visée est la suivante : un code métier plus pérenne et facile à tester de façon isolée, une application plus facile à décliner sous d'autres formes (ex : API secondaire, CLI, ...), une infrastructure plus facile à faire évoluer en fonction des besoins.

Quelques ressources d'introduction :

- (_Recommandé_) [Domain-Driven Design Patterns in Python](https://www.youtube.com/watch?v=Ru2T4fu3bGQ) - Vidéo (1h) d'un exposé à la conférence EuroPython 2018, qui introduit les concepts clés du DDD appliqués au langage Python.
- (_Recommandé_) [L'architecture hexagonale avec Symfony][0] - Introduction en français à l'architecture hexagonale, et un exemple d'intégration dans un contexte web (Symfony).
- [Cosmic Python](https://www.cosmicpython.com/book/preface.html) - Ce livre publié en 2020 traite d'architecture pour les projets Python, en abordant notamment les fondamentaux du DDD et du CQRS.
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Description originale (relativement théorique) de l'architecture hexagonale par Alistair Cockburn.
- [Domain-Driven Design in dynamic languages](https://github.com/valignatev/ddd-dynamic) - Dépôt GitHub de ressources au sujet du DDD appliqué aux langages typés dynamiquement (Python, Ruby, PHP, etc).

[0]: https://www.elao.com/blog/dev/architecture-hexagonale-symfony

## Description

Le dossier `server/` contient notamment les dossiers suivants :

* `domain` - Code métier : entités, règles métier, _repositories_, erreurs, et autres interfaces... Cette partie doit utiliser une terminologie métier, compréhensible par toutes et tous (_ubiquitous language_).
* `application` - Code applicatif : typiquement des commandes (_commands_), requêtes (_queries_), et leurs _handlers_.
* `infrastructure` - Implémentations concrètes faisant le lien entre l'application et l'infrastructure technique.
* `config` - Configuration du serveur et du système d'injection de dépendances (_DI_).
* `api` - Code de l'API REST.
* `seedwork` - Types et interfaces servant de base à l'architecture.

Les dossiers `domain`, `application` et `infrastructure` sont divisés en dossiers thématiques.
