from typing import Callable, NamedTuple
import enum
import requests


LazyResponse = Callable[[], requests.Response]
ArtInfoResponseType = requests.Response | LazyResponse


class ArtworkType(enum.Enum):
    ILLUST = 0  # 插画
    MANGA = 1  # 漫画
    UGORIA = 2  # 动图


class ArtworkTag(NamedTuple):
    name: str
    translation: str


class ArtworkRestrict(enum.Enum):
    NON_R18 = 0
    R18 = 1
    R18G = 2


class RankType(enum.Enum):
    DAILY = 'daily'  # 日榜
    WEEKLY = 'weekly'  # 周榜
    MONTHLY = 'monthly'  # 月榜
    NEWBIE = "rookie"  # 新人榜
    ORIGINAL = "original"  # 原创榜
    DAILY_AI = "daily_ai"  # 日榜-ai
    MALE = "male"  # 男性喜爱
    FEMALE = "female"  # 女性喜爱

    DAILY_R18 = 'daily_r18'
    WEEKLY_R18 = 'weekly_r18'
    WEEKLY_R18G = 'r18g'
    DAILY_AI_R18 = "daily_r18_ai"
    MALE_R18 = "male_r18"
    FEMALE_R18 = "female_r18"
