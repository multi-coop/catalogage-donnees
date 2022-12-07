import asyncio
import functools
import logging.config
from typing import Dict, List, Tuple

import click
from dotenv import load_dotenv

from server.application.datasets.commands import UpdateDataset
from server.config.di import bootstrap, resolve
from server.config.settings import Settings
from server.domain.common.pagination import Page
from server.domain.common.types import ID, Skip
from server.domain.datasets.entities import Dataset
from server.domain.datasets.repositories import DatasetGetAllExtras, DatasetRepository
from server.domain.datasets.specifications import DatasetSpec
from server.domain.tags.entities import Tag
from server.domain.tags.repositories import TagRepository
from server.infrastructure.logging.config import get_log_config
from server.seedwork.application.messages import MessageBus

load_dotenv()
success = functools.partial(click.style, fg="bright_green")
info = functools.partial(click.style, fg="blue")


async def update_dataset_tags(
    dataset_results: List[Tuple[Dataset, DatasetGetAllExtras]],
    dataset_ids_map: Dict[ID, List[ID]],
    bus: MessageBus,
) -> None:

    for dataset, _ in dataset_results:

        if dataset is not None and dataset.id in dataset_ids_map:
            tags = dataset_ids_map[dataset.id]
            await bus.execute(
                UpdateDataset(
                    account=Skip(),
                    tag_ids=tags,
                    **dataset.dict(exclude={"tag_ids"}),
                )
            )


def build_tag_table_of_truth(
    tags: List[Tag], tag_table_of_truth: Dict[str, ID] = {}
) -> Dict[str, ID]:
    for tag in tags:
        if tag.name not in tag_table_of_truth:
            tag_table_of_truth[tag.name] = tag.id

    return tag_table_of_truth


def link_dataset_with_tags_to_keep(
    dataset_results: List[Tuple[Dataset, DatasetGetAllExtras]],
    table_of_truth: Dict[str, ID],
) -> Dict[ID, List[ID]]:
    tags_to_keep: Dict[ID, List[ID]] = {}

    for dataset, _ in dataset_results:
        tags = dataset.tags
        for tag in tags:
            truth = table_of_truth[tag.name]

            if dataset.id not in tags_to_keep.keys():
                tags_to_keep[dataset.id] = [truth]
            else:
                tags_to_keep[dataset.id].append(truth)

    return tags_to_keep


def get_tags_to_delete_list(
    tags: List[Tag],
    table_of_truth: Dict[str, ID],
) -> List[ID]:
    tags_to_delete: List[ID] = []

    def match_with_the_truth(tag: Tag) -> bool:
        return table_of_truth[tag.name] == tag.id

    for tag in tags:
        if not match_with_the_truth(tag):
            tags_to_delete.append(tag.id)

    return tags_to_delete


def build_table_of_truth_from_stored_datasets(
    dataset_results: List[Tuple[Dataset, DatasetGetAllExtras]]
) -> Dict[str, ID]:
    table_of_truth: Dict[str, ID] = {}

    for dataset, _ in dataset_results:
        partial_table_of_truth = build_tag_table_of_truth(
            dataset.tags, tag_table_of_truth=table_of_truth
        )

        table_of_truth = partial_table_of_truth

    return table_of_truth


def build_table_of_truth_from_tags(
    tags: List[Tag], partial_table_of_truth: Dict[str, ID]
) -> Dict[str, ID]:

    return build_tag_table_of_truth(tags, partial_table_of_truth)


async def main() -> None:
    bus = resolve(MessageBus)
    tag_repository = resolve(TagRepository)
    datasets_repository = resolve(DatasetRepository)

    dataset_results, _ = await datasets_repository.get_all(
        spec=DatasetSpec(include_all_datasets=True),
        page=Page(
            number=1,
            size=1000,  # we want to get all datasets from the database
        ),
        account=Skip(),
    )

    tags = await tag_repository.get_all()

    partial_table_of_truth = build_table_of_truth_from_stored_datasets(dataset_results)

    table_of_truth = build_table_of_truth_from_tags(tags, partial_table_of_truth)

    dataset_tags_map = link_dataset_with_tags_to_keep(
        dataset_results, table_of_truth=table_of_truth
    )

    await update_dataset_tags(dataset_results, dataset_tags_map, bus)

    tags_to_delete = get_tags_to_delete_list(tags, table_of_truth)

    await tag_repository.delete_many_by_id(tags_to_delete)

    print(
        f"{success('ok')}: {len(tags_to_delete)} duplicated tags deleted - Previoulsy {len(tags)} were stored, {len(tags) - len(tags_to_delete)} remains"  # noqa E501
    )


if __name__ == "__main__":
    bootstrap()

    settings = resolve(Settings)
    logging.config.dictConfig(get_log_config(settings))

    asyncio.run(main())
