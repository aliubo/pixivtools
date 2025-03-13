from .service import new_pixiv_service


def new_pixiv_crawler(cfg):
    return new_pixiv_service(cfg).crawler()
