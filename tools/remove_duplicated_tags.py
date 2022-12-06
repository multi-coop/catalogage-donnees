import asyncio
import functools
from typing import Dict, List, Tuple


import click
from dotenv import load_dotenv

from server.application.datasets.commands import UpdateDataset
from server.application.tags.views import TagView
from server.config.di import bootstrap, resolve
from server.domain.common.types import ID, Skip
from server.domain.datasets.entities import Dataset
from server.domain.datasets.repositories import DatasetGetAllExtras, DatasetRepository
from server.domain.tags.entities import Tag
from server.domain.tags.repositories import TagRepository
from server.seedwork.application.messages import MessageBus


load_dotenv()
success = functools.partial(click.style, fg="bright_green")


def get_duplicated_tags_ids_to_delelte(tags: List[TagView]) -> List[ID]:
    tags_to_delete = []
    tag_names = []
    for tag in tags:
        if not tag.name in tag_names:
            tag_names.append(tag.name)
        else:
            tags_to_delete.append(tag.id)
    return tags_to_delete


async def update_dataset_tags(
    dataset_results: List[Tuple[Dataset, DatasetGetAllExtras]],
    dataset_ids_map: Dict[ID, List[ID]],
    bus: MessageBus,
) -> None:
    tasks = []
    for dataset, _ in dataset_results:
        tags = dataset_ids_map[dataset.id]
        tasks.append(
            bus.execute(
                UpdateDataset(
                    account=Skip(), tag_ids=tags, **dataset.dict(exclude={"tag_ids"})
                )
            )
        )

    await asyncio.wait(tasks)


def group_tag_by_name(tags: List[Tag]) -> Dict[str, List[ID]]:

    groupped_by_tag_by_name: Dict[str, List[ID]] = {}

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
) -> Dict[ID, List[ID]]:
    tags_to_keep: Dict[ID, List[ID]] = {}

    for dataset, _ in dataset_results:
        tags = dataset.tags
        for tag in tags:
            truth = table_of_truth[tag.name]
            if truth == tag.id:
                if dataset.id in tags_to_keep:
                    tags_to_keep[dataset.id].append(tag.id)
                else:
                    tags_to_keep[dataset.id] = [tag.id]

    return tags_to_keep


def get_tags_to_delete_list(
    dataset_results: List[Tuple[Dataset, DatasetGetAllExtras]],
    table_of_truth: Dict[str, ID],
) -> List[ID]:

    tags_to_remove: List[ID] = []

    for dataset, _ in dataset_results:
        tags = dataset.tags
        for tag in tags:
            truth = table_of_truth[tag.name]
            if not truth == tag.id:
                tags_to_remove.append(tag.id)

    return tags_to_remove


async def main() -> None:
    bus = resolve(MessageBus)
    tag_repository = resolve(TagRepository)
    # datasets_repository = resolve(DatasetRepository)

    # dataset_results, _ = await datasets_repository.get_all()

    # tag_table_of_truth = build_tag_table_of_truth(dataset_results)

    # dataset_tags_map = link_dataset_with_tags_to_keep(
    #     dataset_results, tag_table_of_truth
    # )

    # await update_dataset_tags(dataset_results, dataset_tags_map, bus)

    # tags_to_delete = get_tags_to_delete_list(dataset_results, tag_table_of_truth)

    # await tag_repository.delete_many_by_id(tags_to_delete)

    # tags = await tag_repository.get_all()

    # ids = get_duplicated_tags_ids_to_delelte(tags)

    await tag_repository.delete_many_by_id([])

    # print(f"{success('ok')}: {len(ids)} tags deleted")


if __name__ == "__main__":
    bootstrap()
    asyncio.run(main())
