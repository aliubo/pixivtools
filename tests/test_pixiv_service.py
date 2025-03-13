import unittest
import pixivtools.pixiv_service as pixiv_service
import pixivtools.pixiv_cfg as pixiv_cfg
from .constants import *


class TestPixivService(unittest.TestCase):
    def setUp(self):
        self.service = pixiv_service.new_pixiv_service(pixiv_cfg.load_pixiv_config())
        self.crawler = self.service.crawler()

    def test_get_artwork_info(self):
        for artwork_id in TEST_ARTWORK_IDS:
            self.crawler.get_by_artwork_id(artwork_id)


if __name__ == '__main__':
    unittest.main()
