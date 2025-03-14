import pixivtools


def get_config():
    # Create config using constructor
    cfg_maker = pixivtools.pixiv_config_maker()
    # Replace YOUR_PHPSESSID with your actual PHPSESSID from pixiv
    cfg_maker.set_phpsessid("YOUR_PHPSESSID")
    cfg_maker.set_proxy("127.0.0.1:7890")
    cfg_maker.set_img_dir("./out/imgs")
    cfg_maker.set_log_file("./out/out.log")
    cfg_maker.set_sql_url("sqlite:///pixiv.db")  # other db url see ./config.yaml or https://docs.sqlalchemy.org/en/20/core/engines.html
    return cfg_maker()

def run_constructor_example():
    """Example: Using constructor to create crawler"""    # Create service and crawler
    cfg = get_config()
    service = pixivtools.new_pixiv_service(cfg)
    crawler = service.crawler()
    
    # Example crawling tasks
    # 1. Get artwork by ID
    crawler.get_by_artwork_id(98538269)
    
    # 2. Get latest artworks from followed artists (page 1)
    crawler.get_by_follow_latest(1)
    
    # 3. Get artworks from specific user
    crawler.get_by_user_id(23279364)
    
    # 4. Get popular artworks with tag
    crawler.get_by_tag_popular("ホロライブ")

if __name__ == "__main__":
    run_constructor_example() 