import unittest
from pixivtools.pixiv_api import PixivApi, new_filter, RankType
import pixivtools.pixiv_cfg as pixiv_cfg
import datetime
from .constants import *


class TestPixivApi(unittest.TestCase):
    def setUp(self):
        cfg = pixiv_cfg.load_pixiv_config()
        self.api = PixivApi(cfg.api)
        self.options = new_filter()

    def test_get_artwork_info(self):
        for artwork_id in TEST_ARTWORK_IDS:
            artwork_info = self.api.get_artwork_info(artwork_id, self.options)
            #print(artwork_info.__str__(wrap=True, detail=False))
            self.assertIsNotNone(artwork_info)
            self.assertEqual(artwork_info.artwork_id, artwork_id)

    def test_get_artworks_by_userid(self):
        for user_id in TEST_USER_IDS:
            artworks = self.api.get_artworks_by_userid(user_id, self.options)
            #print(artworks)
            self.assertIsInstance(artworks, dict)
            self.assertGreater(len(artworks), 0)

    def test_get_artworks_by_follow_latest(self):
        for page in range(1, 3):
            artworks = self.api.get_artworks_by_follow_latest(page, self.options)
            #print(artworks)
            self.assertIsInstance(artworks, dict)
            self.assertGreater(len(artworks), 0)

    def test_get_artworks_by_pixivision_aid(self):
        for aid in TEST_PIXIVISION_AIDS:
            pixivision_info = self.api.get_artworks_by_pixivision_aid(aid, self.options)
            #print(pixivision_info)
            self.assertIsNotNone(pixivision_info)
            self.assertEqual(pixivision_info.aid, aid)

    def test_get_image(self):
        for artwork_id in TEST_ARTWORK_IDS:
            artwork_info = self.api.get_artwork_info(artwork_id, self.options)
            test_imgs = list(artwork_info.image_download_urls)
            if len(test_imgs) > 1:
                test_imgs = [test_imgs[0], test_imgs[-1]]
            for url in test_imgs:
                image_data = self.api.get_image(url.small)
                #print(f"url: {url.small}, image_len: {len(image_data)}")
                self.assertIsInstance(image_data, bytes)
                self.assertGreater(len(image_data), 0)

    def test_get_artworks_by_recommend(self):
        artworks = self.api.get_artworks_by_recommend(self.options)
        #print(artworks)
        self.assertIsInstance(artworks, dict)
        self.assertGreater(len(artworks), 0)

    def test_get_artworks_by_rank(self):
        test_lst = [RankType.DAILY, RankType.WEEKLY_R18, RankType.WEEKLY]
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
        #print(yesterday)
        for rank_type in test_lst:
            artworks = self.api.get_artworks_by_rank(rank_type, yesterday, 1, self.options)
            #print(artworks)
            self.assertIsInstance(artworks, dict)
            self.assertGreater(len(artworks), 0)

    def test_get_artworks_by_request_recommend(self):
        artworks = self.api.get_artworks_by_request_recommend(self.options)
        #print(artworks)
        self.assertIsInstance(artworks, dict)
        self.assertGreater(len(artworks), 0)
    
    def test_get_userids_by_request_creator(self):
        user_ids = self.api.get_userids_by_request_creator(self.options)
        #print(user_ids)
        self.assertIsInstance(user_ids, list)
        self.assertGreater(len(user_ids), 0)

    def test_get_userids_by_similar_user(self):
        for user_id in TEST_USER_IDS:
            user_ids = self.api.get_userids_by_similar_user(user_id, self.options)
            #print(user_ids)
            self.assertIsInstance(user_ids, list)
            self.assertGreater(len(user_ids), 0)

    def test_get_artworks_by_user_bookmark(self):
        for user_id in TEST_USER_IDS:
            artworks = self.api.get_artworks_by_user_bookmark(user_id, 1, self.options)
            #print(artworks)
            self.assertIsInstance(artworks, dict)
            self.assertGreater(len(artworks), 0)

    def test_get_artworks_by_tag_popular(self):
        for tag in TEST_TAGS:
            artworks = self.api.get_artworks_by_tag_popular(tag, self.options)
            #print(artworks)
            self.assertIsInstance(artworks, dict)
            self.assertGreater(len(artworks), 0)

    def test_get_userids_by_recommend(self):
        user_ids = self.api.get_userids_by_recommend(self.options)
        #print(user_ids)
        self.assertIsInstance(user_ids, list)
        self.assertGreater(len(user_ids), 0)

    def test_get_artworks_by_similar_artwork(self):
        for artwork_id in TEST_ARTWORK_IDS:
            artworks = self.api.get_artworks_by_similar_artwork(artwork_id, self.options)
            #print(artworks)
            self.assertIsInstance(artworks, dict)
            self.assertGreater(len(artworks), 0)

if __name__ == '__main__':
    unittest.main()
