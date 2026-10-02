import os
import asyncio
import logging
from pathlib import Path

from ossapi import OssapiAsync
from dotenv import load_dotenv

from search import search_all_beatmaps, SearchCriteria
from downloader import download_all
from exceptions import MissingEnvironmentVariableError
from logging_config import setup_logging

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DOWNLOAD_PATH = Path.home() / "Downloads" / "beatmaps"

logger = logging.getLogger(__name__)


def get_credentials() -> tuple[int, str]:
    if CLIENT_ID is None or CLIENT_SECRET is None:
        raise MissingEnvironmentVariableError(
            "CLIENT_ID and CLIENT_SECRET must be defined."
        )
    return int(CLIENT_ID), CLIENT_SECRET


async def main() -> None:
    setup_logging()
    logger.info("Starting osu! downloader")

    client_id, client_secret = get_credentials()
    api = OssapiAsync(client_id, client_secret)

    criteria = SearchCriteria()

    beatmapset_ids = await search_all_beatmaps(api, criteria)
    await download_all(beatmapset_ids, DOWNLOAD_PATH)


if __name__ == "__main__":
    asyncio.run(main())
