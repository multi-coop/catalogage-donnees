# Outil de catalogage de données

[![CI](https://github.com/etalab/catalogage-donnees/actions/workflows/ci.yml/badge.svg)](https://github.com/etalab/catalogage-donnees/actions/workflows/ci.yml)

Cet outil en cours de développement permettra à des organisations de gérer le catalogue des données qu'elles produisent.

L'équipe projet a été formée en décembre 2021 à la suite d'une [investigation](https://jailbreak.gitlab.io/investigation-catalogue/synthese.html) visant à comprendre les besoins fonctionnels à adresser pour cataloguer les données d'une administration.

## Implémentation

Le cas d'usage pour lequel cet outil est développé est un service permettant aux ministères et aux opérateurs sous leur tutelle de créer, gérer et ouvrir leurs catalogues dans le cadre notamment de [leur stratégie en matière de politique de la donnée](https://www.etalab.gouv.fr/politique-de-la-donnee-des-algorithmes-et-des-codes-sources-15-strategies-ministerielles-et-500-actions-pour-accelerer/).

La première instance de l'outil sera le service connu sous le nom de `catalogue.data.gouv.fr`, coordonné par la DINUM. La configuration de cette instance (organisations et leur catalogue) est gérée dans un dépôt dédié : https://github.com/etalab/catalogage-donnees-config.

Les catalogues de données qui seront ouverts grâce à ce service contiennent des informations (métadonnées) sur des données inventoriées mais qui elles-mêmes n'ont pas encore été ouvertes sous formes de jeux de données sur [data.gouv.fr](https://www.data.gouv.fr/fr/).

## Schéma

Le catalogue des données d'une organisation est défini par un [schéma commun](https://github.com/etalab/schema-catalogue-donnees), avec ou sans champs complémentaires.

## Démarrage rapide

Pour démarrer l'application (http://localhost:3000) :

```
make compose-up
```

Pour plus d'informations, consultez [le guide de démarrage rapide](./docs/fr/demarrage.md).

## Démo

Une instance de démonstration de l'application est accessible sur [demo.catalogue.multi.coop](http://demo.catalogue.multi.coop/). Login : `catalogue.demo@yopmail.com `, mot de passe : `password1234`.

## Contribuer

Consultez [la documentation de développement](./docs/fr/README.md).

## Licence

AGPL 3.0
