import asyncio
from typing import Dict, List, Tuple

from server.config.di import bootstrap, resolve
from server.domain.common.types import ID
from server.domain.datasets.entities import Dataset
from server.domain.datasets.repositories import DatasetGetAllExtras, DatasetRepository
from server.domain.tags.entities import Tag
from server.domain.tags.repositories import TagRepository
from server.seedwork.application.messages import MessageBus


def group_tag_by_name(tags: List[Tag]) -> Dict[str, List[str]]:

    groupped_by_tag_by_name: Dict[str, List[str]] = {}

    for tag in tags:
        if tag.name in groupped_by_tag_by_name:
            groupped_by_tag_by_name[tag.name].append(tag.id)
        else:
            groupped_by_tag_by_name[tag.name] = [tag.id]

    return groupped_by_tag_by_name


def build_tag_table_of_truth(
    dataset_results: List[Tuple[Dataset, DatasetGetAllExtras]]
) -> Dict[str, ID]:

    tag_table_of_truth: Dict[str, ID] = {}

    for dataset, _ in dataset_results:
        tags = dataset.tags
        for tag in tags:
            if tag.name not in tag_table_of_truth:
                tag_table_of_truth[tag.name] = tag.id

    return tag_table_of_truth


def link_dataset_with_tags_to_keep(
    dataset_results: List[Tuple[Dataset, DatasetGetAllExtras]],
    table_of_truth: Dict[str, ID],
) -> Dict[ID, Tuple[Dataset, List[str]]]:
    for dataset, _ in dataset_results:
        pass


async def main() -> None:
    bus = resolve(MessageBus)
    tag_repository = resolve(TagRepository)
    datasets_repository = resolve(DatasetRepository)

    tags = await tag_repository.get_all()
    results = await datasets_repository.get_all()

    groupped_by_tag_by_name = group_tag_by_name(tags)

    # Table of truth
    #  name => id
    #
    #
    #

    # Création de la table de vérite
    # Pour chaque datasets
    #   Récupérer les tags du dataset
    #   Pour chaque tag du dataset
    #       Est-ce que le tag est dans la table de vérité
    #           Non, on ajoute le tag dans la table de vériTé
    #           Oui
    #               Est-ce que l'id du tag correspond à l'id de la table de vérité
    #                   Oui, on ajoute l'id du tag dans le tableau des tags à garder pour le dataset
    #                   Non, on passe au suivant
    #
    #
    #

    tag_table_of_truth: Dict[str, ID] = {}
    tags_to_keep: Dict[ID, Tuple[Dataset, List[str]]] = {}

    dataset_results = results[0]

    tag_table_of_truth = build_tag_table_of_truth(dataset_results)

    breakpoint()

    # for key, value in groupped_by_tag_by_name.items():
    #     if len(value) > 1:
    #         duplicated_ids = duplicated_ids + value[1:]

    # await tag_repository.delete_many_by_id(duplicated_ids)


if __name__ == "__main__":
    bootstrap()
    asyncio.run(main())
