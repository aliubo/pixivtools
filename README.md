# pixivtools

[中文文档](README_zh.md)

A tool for crawling images from pixiv website, supporting multiple crawling modes

## Supported Features

* Download images by artwork id
* Download images by artist id (userid)
* Download images by pixivision id (pixivision site)
* Download latest uploads from followed artists
* Download recommended works from homepage
* Download images from rankings
* Download recommended works from commission section
* Download images from user's bookmarks
* Download popular works by specified tags
* Download similar works by specified artwork id
* Download works from all similar artists of a specified artist id
* Download works from platform-recommended artists
* Download works from latest commission artists

## Usage

### 1. Install pixivtools
```shell
pip install pixivtools --upgrade
```

### 2. Create Configuration Object

There are two ways to set up the configuration, choose according to your preference

#### 1) Create through Constructor
```python
import pixivtools

cfg_maker = pixivtools.pixiv_config_maker()
# Adjust according to your needs
cfg_maker.set_phpsessid("Enter your pixiv PHPSESSID")
cfg_maker.set_proxy("127.0.0.1:7890")
cfg_maker.set_img_dir("./imgs")             # Location to store images
cfg_maker.set_log_file("./out.log")         # Location for log output
cfg_maker.set_sql_url("sqlite:///pixiv.db") # SQLAlchemy format connection URL, can be ignored if not understood
cfg = cfg_maker()
```

#### 2) Through Configuration File
Create a `config.yaml` file, see `config.yaml.example` in the repository for configuration example

Then use `cfg = pixivtools.load_pixiv_config("config.yaml")`


### 3. Start Operations
```python
# Pass the cfg object obtained from the previous step
service = pixivtools.new_pixiv_service(cfg)
# Get crawler instance
crawler = service.crawler()
# Examples of different crawling modes
crawler.get_by_artwork_id(98538269)
crawler.get_by_user_id(23279364)
crawler.get_by_pixivision_aid(9374)
crawler.get_by_follow_latest(1)
crawler.get_by_recommend()
crawler.get_by_rank(pixivtools.RankType.MONTHLY, 20250313, 1)
crawler.get_by_request_recommend()
crawler.get_by_user_bookmark(92803629, 1)
crawler.get_by_tag_popular("ホロライブ")
crawler.get_by_similar_artwork(115812789)
crawler.get_by_similar_user(20015785)
crawler.get_by_recommend_user()
crawler.get_by_request_creator()
```

### 4. After crawling is complete, images will be saved to the specified path, and the database will record all related metadata for your use 