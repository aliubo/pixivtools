import pathlib
from typing import NamedTuple, Optional
import yaml


class ApiMetaArgument(NamedTuple):
    phpsessid: str
    proxy: str


class CrawlerConfig(NamedTuple):
    img_dir: pathlib.Path
    sql_url: str


class PixivConfig(NamedTuple):
    api: ApiMetaArgument
    crawler: CrawlerConfig
    log_file: pathlib.Path


class PixivConfigMaker:    
    def __init__(self):
        # API配置
        self._phpsessid: Optional[str] = ""
        self._proxy: Optional[str] = ""
        
        # 爬虫配置
        self._img_dir: Optional[pathlib.Path] = "out/imgs"
        self._sql_url: Optional[str] = "sqlite:///out/pixiv.db"
        
        # 日志配置
        self._log_file: Optional[pathlib.Path] = "out/out.log"
    
    def set_phpsessid(self, phpsessid: str):
        self._phpsessid = phpsessid
        return self
    
    def set_proxy(self, proxy: str):
        self._proxy = proxy
        return self
    
    def set_img_dir(self, img_dir: str | pathlib.Path):
        if isinstance(img_dir, str):
            img_dir = pathlib.Path(img_dir)
        
        if not img_dir.exists():
            img_dir.mkdir(parents=True)
            
        self._img_dir = img_dir
        return self
    
    def set_sql_url(self, sql_url: str):
        self._sql_url = sql_url
        return self
    
    def set_log_file(self, log_file: str | pathlib.Path):
        if isinstance(log_file, str):
            log_file = pathlib.Path(log_file)
        
        log_dir = log_file.parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True)
            
        self._log_file = log_file
        return self
    
    def __call__(self) -> PixivConfig:
        obj = {
            "api": {
                "phpsessid": self._phpsessid,
                "proxy": self._proxy
            },
            "crawler": {
                "img_dir": str(self._img_dir),
                "sql_url": self._sql_url
            },
            "log_file": str(self._log_file)
        }
        return _load_config(obj)



def pixiv_config_maker() -> PixivConfigMaker:
    return PixivConfigMaker()


def load_pixiv_config(filename: str) -> PixivConfig:
    cfg_path = pathlib.Path() / filename
    if not cfg_path.exists():
        raise FileNotFoundError(f"文件{cfg_path.absolute}不存在")
    with open(cfg_path, "r") as f:
        obj = yaml.safe_load(f)
    return _load_config(obj)


def _load_config(obj: dict) -> PixivConfig:
    log_file_path = pathlib.Path() / obj["log_file"]
    log_file_dir = log_file_path.parent
    if not log_file_dir.exists():
        log_file_dir.mkdir(parents=True)

    def _load_crawler_config(crawler_obj: dict) -> CrawlerConfig:
        img_file_dir = pathlib.Path() / crawler_obj["img_dir"]
        if not img_file_dir.exists():
            img_file_dir.mkdir(parents=True)

        crawler_obj["img_dir"] = img_file_dir
        return CrawlerConfig(**crawler_obj)

    return PixivConfig(
        api=ApiMetaArgument(**obj["api"]),
        crawler=_load_crawler_config(obj["crawler"]),
        log_file=log_file_path
    )
