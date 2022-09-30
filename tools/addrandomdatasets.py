import argparse
import asyncio
import functools
import random

import click
from tqdm import tqdm

from server.application.tags.queries import GetAllTags
from server.config.di import bootstrap, resolve
from server.domain.common.types import Skip
from server.domain.organizations.types import Siret
from server.seedwork.application.messages import MessageBus
from tests.factories import CreateDatasetFactory

success = functools.partial(click.style, fg="bright_green")


async def main(n: int, siret: Siret) -> None:
    bus = resolve(MessageBus)

    tag_id_set = [tag.id for tag in await bus.execute(GetAllTags())]
    assert len(tag_id_set) >= 1, "Need at least 1 tag in DB, 0 found"

    for _ in tqdm(range(n), unit="dataset"):
        tag_ids = random.choices(
            tag_id_set, k=random.randint(1, min(3, len(tag_id_set)))
        )
        await bus.execute(
            CreateDatasetFactory.build(
                account=Skip(), organization_siret=siret, tag_ids=tag_ids
            )
        )

    print(f"{success('created')}: {n} datasets")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("siret", type=Siret)
    args = parser.parse_args()

    bootstrap()
    asyncio.run(main(n=args.n, siret=args.siret))
