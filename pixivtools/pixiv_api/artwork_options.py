from typing import Optional, TypedDict
from .struct import *


class ArtworkOptions(TypedDict):
    # update: bool, 是否更新已存在的artwork
    update: bool
    # only_r18: bool, 是否只爬取R18
    only_r18: bool
    # only_non_r18: bool, 是否只爬取非R18
    only_non_r18: bool
    # skip_manga: bool, 是否跳过漫画
    skip_manga: bool
    # artwork_types: list[ArtworkType], 只爬取指定类型的artwork
    artwork_types: list[ArtworkType] | None
    # ignore_error: bool, 是否忽略爬取过程中的某个artwork出错，如果为False则会在出错时直接raise
    ignore_error: bool


def is_skip(options: ArtworkOptions, artwork_info) -> Optional[str]:
    if options['only_r18'] and artwork_info.restrict == ArtworkRestrict.NON_R18:
        return "only_r18"
    if options['only_non_r18'] and artwork_info.restrict != ArtworkRestrict.NON_R18:
        return "only_non_r18"
    if options['skip_manga'] and artwork_info.artwork_type == ArtworkType.MANGA:
        return "skip_manga"
    if options['artwork_types'] and artwork_info.artwork_type not in options['artwork_types']:
        return "artwork_types"


def _default_filter() -> ArtworkOptions:
    return ArtworkOptions(
        update=False,
        only_r18=False,
        only_non_r18=False,
        skip_manga=True,
        artwork_types=None,
        ignore_error=True
    )


def new_filter(**kwargs: ArtworkOptions) -> ArtworkOptions:
    res = _default_filter()
    res.update(kwargs)
    return res
