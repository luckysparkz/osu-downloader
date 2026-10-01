import os
import asyncio

from ossapi import OssapiAsync
from dotenv import load_dotenv

from exceptions import MissingEnvironmentVariableError

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_credentials() -> tuple[int, str]:
    if CLIENT_ID is None or CLIENT_SECRET is None:
        raise MissingEnvironmentVariableError(
            "CLIENT_ID and CLIENT_SECRET must be defined."
        )
    return int(CLIENT_ID), CLIENT_SECRET


async def main() -> None:
    client_id, client_secret = get_credentials()
    api = OssapiAsync(client_id, client_secret)
    beatmapset = await api.beatmapset(297969)
    print(beatmapset.title)


if __name__ == "__main__":
    asyncio.run(main())
