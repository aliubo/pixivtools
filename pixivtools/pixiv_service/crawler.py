import pixivtools.pixiv_api as pixiv_api
from . import model
from .context import PixivContext
from pathlib import Path
from PIL import Image
import io
from typing import Sequence


class PixivCrawler:
    def __init__(self, context: PixivContext):
        self._api = context.api
        self._sql = context.sql
        self._img_dir = context.img_dir
        self._log = context.log

    def _new_artwork(
            self,
            artwork_info: pixiv_api.ArtworkInfo,
            tags: Sequence[model.Tag],
    ) -> model.Artwork:
        return model.Artwork(
            artwork_id=artwork_info.artwork_id,
            user_id=artwork_info.user_id,
            artwork_type=artwork_info.artwork_type.value,
            title=artwork_info.title,
            nums=artwork_info.nums,
            restrict=artwork_info.restrict.value,
            description=artwork_info.desc,
            bookmark_cnt=artwork_info.bookmark_cnt,
            like_cnt=artwork_info.like_cnt,
            comment_cnt=artwork_info.comment_cnt,
            view_cnt=artwork_info.view_cnt,
            create_time=artwork_info.create_time,
            upload_time=artwork_info.upload_time,
            tags=tags,
        )

    def _get_filepath(self, artwork_id: int, idx: int) -> Path:
        return self._img_dir / f"{artwork_id}_{idx}.jpg"

    def _download_artwork(self, artwork_info: pixiv_api.ArtworkInfo) -> list[model.Image]:
        res = []
        for idx, url in enumerate(artwork_info.image_download_urls):
            file_path = self._get_filepath(artwork_info.artwork_id, idx)
            if file_path.exists() and file_path.stat().st_size > 0:
                with Image.open(file_path) as img:
                    width, height = img.size
                res.append(model.Image(
                    artwork_id=artwork_info.artwork_id,
                    idx=idx,
                    height=height,
                    width=width,
                    file_size=file_path.stat().st_size
                ))
                continue
            content = self._api.get_image(url.original)
            with Image.open(io.BytesIO(content)) as img:
                width, height = img.size
            res.append(model.Image(
                artwork_id=artwork_info.artwork_id,
                idx=idx,
                height=height,
                width=width,
                file_size=len(content)
            ))
            with file_path.open('wb+') as f:
                f.write(content)
        return res

    def _is_artwork_exist(self, artwork_id: int) -> bool:
        with self._sql() as session:
            artwork_record = session.query(model.Artwork).filter_by(artwork_id=artwork_id).first()
            if not artwork_record:
                return False
        for idx in range(artwork_record.nums):
            file_path = self._get_filepath(artwork_id, idx)
            if not file_path.exists() or file_path.stat().st_size <= 0:
                return False
        return True

    def _get_by_artwork_info(
            self,
            artwork_info: pixiv_api.ArtworkInfo,
            options: pixiv_api.ArtworkOptions | None = None
    ) -> bool:
        if options is None:
            options = pixiv_api.new_filter()

        invalid_reason = pixiv_api.is_skip(options, artwork_info)
        if invalid_reason:
            self._log.info(f"artwork {artwork_info.artwork_id} is invalid, reason: {invalid_reason}")
            return False

        if self._is_artwork_exist(artwork_info.artwork_id):
            if not options["update"]:
                self._log.info(f"artwork {artwork_info.artwork_id} already exist")
                return False
        # 爬取图片
        add_images = self._download_artwork(artwork_info)
        # 存数据库
        with self._sql() as session:
            tags = []
            imgs = []
            for tag in artwork_info.tags:
                tag_record = session.query(model.Tag).filter_by(name=tag.name).first()
                if tag_record is None:
                    tags.append(model.Tag(name=tag.name, trans_name=tag.translation))
                else:
                    tags.append(tag_record)
            user = model.User(user_id=artwork_info.user_id, user_name=artwork_info.user_name)
            session.merge(user)
            artwork = self._new_artwork(artwork_info, tags)
            session.merge(artwork)  # 会自动插入不存在的tag
            for img in add_images:
                img_record = session.query(model.Image).filter_by(artwork_id=img.artwork_id, idx=img.idx).first()
                if img_record is None:
                    imgs.append(img)
                else:
                    imgs.append(img_record)
            session.add_all(imgs)

            session.commit()
        return True

    def _get_by_artworks_info(
            self,
            artworks_info: dict[int, pixiv_api.ArtworkInfo],
            options: pixiv_api.ArtworkOptions) -> list[int]:
        self._log.info("Artworks start downloading...", artworks=artworks_info.keys())
        ok_ids = []
        for idx, (artwork_id, artwork_info) in enumerate(artworks_info.items()):
            self._log.info(f"{idx+1}/{len(artworks_info)} - {artwork_id}")
            try:
                if self._get_by_artwork_info(artwork_info, options):
                    ok_ids.append(artwork_id)
            except Exception as e:
                self._log.error(f"save artwork {artwork_id} failed", error=str(e))
                if not options["ignore_error"]:
                    raise e
                continue
            self._log.info(
                f"save artwork {artwork_id} to database",
                title=artwork_info.title,
                tags=[tag.name for tag in artwork_info.tags],
                user=f"{artwork_info.user_name}({artwork_info.user_id})",
                nums=artwork_info.nums
            )
        self._log.info("Artworks download finished", failed_ids=[i for i in artworks_info.keys() if i not in ok_ids])
        return ok_ids

    def get_by_artwork_id(self, artwork_id: int, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        artwork_info = self._api.get_artwork_info(artwork_id, options)
        self._get_by_artwork_info(artwork_info, options)
        self._log.info(
            f"save artwork {artwork_info.artwork_id} to database",
            title=artwork_info.title,
            tags=[tag.name for tag in artwork_info.tags],
            user=f"{artwork_info.user_name}({artwork_info.user_id})",
        )

    def get_by_user_id(self, user_id: int, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()
        artworks = self._api.get_artworks_by_userid(user_id, options)
        self._log.info("get artworks from user", user_id=user_id)
        self._get_by_artworks_info(artworks, options)

    def _get_by_users_id(self, user_ids: list[int], options: pixiv_api.ArtworkOptions):
        self._log.info("Users start downloading...", user_ids=user_ids)
        for idx, user_id in enumerate(user_ids):
            self._log.info(f"! {idx + 1}/{len(user_ids)} start to save user {user_id} to database")
            self.get_by_user_id(user_id, options)
        self._log.info("Users download finished")

    def get_by_pixivision_aid(self, aid: int, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        res = self._api.get_artworks_by_pixivision_aid(aid, options)
        self._log.info(f"get artworks from pixivision", aid=aid, title=res.title, type=res.pixivision_type)
        get_ids = self._get_by_artworks_info(res.artworks, options)
        with self._sql() as session:
            pixivision = model.Pixivision(
                aid=aid,
                title=res.title,
                type=res.pixivision_type,
                description=res.desc,
                artworks=[
                    session.query(model.Artwork).filter_by(artwork_id=artwork_id).first()
                    for artwork_id in get_ids
                ]
            )
            session.merge(pixivision)
            session.commit()
        self._log.info(f"save pixivision {aid} to database")

    def get_by_follow_latest(self, page: int, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        artworks = self._api.get_artworks_by_follow_latest(page, options)
        self._log.info(f"get artworks from bookmark new", page=page)
        self._get_by_artworks_info(artworks, options)

    def get_by_recommend(self, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        artworks: dict[int, pixiv_api.ArtworkInfo] = self._api.get_artworks_by_recommend(options)
        self._log.info(f"get artworks from recommend")
        self._get_by_artworks_info(artworks, options)

    def get_by_rank(self, rank_type: pixiv_api.RankType, date: int, page: int, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        artworks: dict[int, pixiv_api.ArtworkInfo] = self._api.get_artworks_by_rank(rank_type, date, page, options)
        self._log.info(f"get artworks from rank", rank_type=rank_type.name, date=date, page=page)
        self._get_by_artworks_info(artworks, options)

    def get_by_request_recommend(self, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        artworks: dict[int, pixiv_api.ArtworkInfo] = self._api.get_artworks_by_request_recommend(options)
        self._log.info(f"get artworks from request recommend")
        self._get_by_artworks_info(artworks, options)

    def get_by_user_bookmark(self, user_id: int, page: int, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        artworks: dict[int, pixiv_api.ArtworkInfo] = self._api.get_artworks_by_user_bookmark(user_id, page, options)
        self._log.info(f"get artworks from user bookmark", user_id=user_id, page=page)
        self._get_by_artworks_info(artworks, options)

    def get_by_tag_popular(self, tag_name: str, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        artworks: dict[int, pixiv_api.ArtworkInfo] = self._api.get_artworks_by_tag_popular(tag_name, options)
        self._log.info(f"get artworks from tag popular", tag_name=tag_name)
        self._get_by_artworks_info(artworks, options)

    def get_by_similar_artwork(self, artwork_id: int, options: pixiv_api.ArtworkOptions = None):
        if options is None:
            options = pixiv_api.new_filter()

        artworks: dict[int, pixiv_api.ArtworkInfo] = self._api.get_artworks_by_similar_artwork(artwork_id, options)
        self._log.info(f"get artworks from similar artwork_info", artwork_id=artwork_id)
        self._get_by_artworks_info(artworks, options)

    def get_by_similar_user(self, user_id: int, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        userids: list[int] = self._api.get_userids_by_similar_user(user_id, options)
        self._log.info(f"get similar user from user {user_id}", user_id=user_id)
        self._get_by_users_id(userids, options)

    def get_by_recommend_user(self, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        userids: list[int] = self._api.get_userids_by_recommend(options)
        self._log.info(f"get recommend user")
        self._get_by_users_id(userids, options)

    def get_by_request_creator(self, options: pixiv_api.ArtworkOptions | None = None):
        if options is None:
            options = pixiv_api.new_filter()

        userids: list[int] = self._api.get_userids_by_request_creator(options)
        self._log.info(f"get request creator")
        self._get_by_users_id(userids, options)
