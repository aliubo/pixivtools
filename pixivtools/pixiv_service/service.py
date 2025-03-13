from .crawler import PixivCrawler
from .context import new_context
import pixivtools.pixiv_cfg as cfg


class PixivService():
    def __init__(self, cfg: cfg.PixivConfig):
        self._context = new_context(cfg)
        self._crawler = None

    def crawler(self) -> PixivCrawler:
        if self._crawler:
            return self._crawler
        self._crawler = PixivCrawler(self._context)
        return self._crawler
    
    def sql(self):
        return self._context.sql
    
    def api(self):
        return self._context.api


def new_pixiv_service(cfg: cfg.PixivConfig) -> PixivService:
    return PixivService(cfg)
