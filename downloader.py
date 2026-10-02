import asyncio
import logging
from pathlib import Path

import httpx

MIRROR_URL = "https://mirror.nekoha.moe/api/download/{id}"
TIMEOUT = 30.0
DEFAULT_CONCURRENCY = 4

logger = logging.getLogger(__name__)


async def download_one(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    beatmapset_id: int,
    dest_dir: Path,
) -> bool:
    filepath = dest_dir / f"{beatmapset_id}.osz"
    if filepath.exists():
        logger.info(f"Skipping {beatmapset_id}: already downloaded")
        return True

    async with semaphore:
        try:
            url = MIRROR_URL.format(id=beatmapset_id)
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                with open(filepath, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)
            logger.info(f"Downloaded {beatmapset_id}")
            return True
        except httpx.HTTPError:
            logger.warning(
                f"Download failed for {beatmapset_id}. Skipping beatmap", exc_info=True
            )
            return False


async def download_all(
    beatmapset_ids: list[int], dest_dir: Path, max_concurrent: int = DEFAULT_CONCURRENCY
) -> list[int]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(max_concurrent)

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        tasks = [download_one(client, semaphore, id, dest_dir) for id in beatmapset_ids]
        results = await asyncio.gather(*tasks)

    failed = [bid for bid, ok in zip(beatmapset_ids, results) if not ok]
    return failed
