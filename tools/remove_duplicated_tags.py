import asyncio
from typing import Dict, List

from server.config.di import bootstrap, resolve
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


async def main() -> None:
    bus = resolve(MessageBus)
    tag_repository = resolve(TagRepository)

    tags = await tag_repository.get_all()

    groupped_by_tag_by_name = group_tag_by_name(tags)

    duplicated_ids: List[str] = []

    for key, value in groupped_by_tag_by_name.items():
        if len(value) > 1:
            duplicated_ids = duplicated_ids + value[1:]

    await tag_repository.delete_many_by_id(duplicated_ids)


if __name__ == "__main__":
    bootstrap()
    asyncio.run(main())
