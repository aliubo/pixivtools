# pixiv_crawler

爬取pixiv网站的图片，支持多种爬取模式

## 支持爬取功能

* 按照artwork id下载图片
* 按照画师id(userid)下载图片
* 按照pixivision id下载图片(pixvision站)
* 按照关注的画师最新上传下载图片
* 按照首页推荐的作品下载图片
* 按照排行榜下载图片
* 按照接稿的推荐作品下载图片
* 按照用户的收藏下载图片
* 按照指定标签的热门作品下载图片
* 按照指定的artwork id的相似作品下载图片
* 按照指定的画师id的所有相似画师下载图片
* 按照平台推荐的画师下载图片
* 按照接稿的最新接稿画师下载图片

## 使用方法

### 1、安装pixivtools
```shell
pip install pixivtools --upgrade
```

### 2、创建配置对象

这里有两种办法可以完成配置的设置，可根据喜好选择

#### 1) 通过构造器创建
```python
import pixivtools

cfg_maker = pixivtools.pixiv_config_maker()
# 可根据自己需要做调整
cfg_maker.set_phpsessid("输入pixiv的PHPSESSID")
cfg_maker.set_proxy("127.0.0.1:7890")
cfg_maker.set_img_dir("out/imgs")
cfg_maker.set_sql_url("sqlite:///out/pixiv.db")
cfg_maker.set_log_file("out/out.log")
cfg = cfg_maker()
```

#### 2) 通过配置文件
创建一个`config.yaml`文件，配置示例参见仓库的`config.yaml.example`

然后 `cfg = pixivtools.load_pixiv_config("config.yaml")`


### 3. 开始操作
```python
# 将上一步得到的cfg对象，传到这里
service = pixivtools.new_pixiv_service(cfg)
# 获取爬虫实例
crawler = service.crawler()
# 不同爬取模式的示例
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

### 4. 爬取完成后，图片会保存到指定路径，数据库会记录所有相关的元信息，可根据自行需求食用

