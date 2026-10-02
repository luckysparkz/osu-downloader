from datetime import date
from dataclasses import dataclass, asdict, field

from ossapi import OssapiAsync
from ossapi.ossapiv2_async import (
    BeatmapsetSearchModeT,
    BeatmapsetSearchCategoryT,
    BeatmapsetSearchExplicitContentT,
    BeatmapsetSearchGenreT,
    BeatmapsetSearchLanguageT,
)
from ossapi.enums import (
    BeatmapsetSearchMode,
    BeatmapsetSearchCategory,
    BeatmapsetSearchExplicitContent,
    BeatmapsetSearchGenre,
    BeatmapsetSearchLanguage,
)


def default_query() -> str:
    first_day = date.today().replace(day=1)
    return f"created>={first_day}"


@dataclass
class SearchCriteria:
    query: str = field(default_factory=default_query)
    mode: BeatmapsetSearchModeT = BeatmapsetSearchMode.ANY
    category: BeatmapsetSearchCategoryT = BeatmapsetSearchCategory.HAS_LEADERBOARD
    explicit_content: BeatmapsetSearchExplicitContentT = (
        BeatmapsetSearchExplicitContent.HIDE
    )
    genre: BeatmapsetSearchGenreT = BeatmapsetSearchGenre.ANY
    language: BeatmapsetSearchLanguageT = BeatmapsetSearchLanguage.ANY


async def search_all_beatmaps(api: OssapiAsync, criteria: SearchCriteria) -> list[int]:
    all_ids: list[int] = []
    cursor = None

    while True:
        results = await api.search_beatmapsets(
            **asdict(criteria),
            cursor=cursor,
        )
        all_ids.extend(bs.id for bs in results.beatmapsets)

        if results.cursor is None:
            break
        cursor = results.cursor

    return all_ids
