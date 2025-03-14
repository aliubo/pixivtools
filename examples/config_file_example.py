import pixivtools

def run_config_file_example():
    """Example: Using config file to create crawler"""
    # Make sure you have config.yaml file with proper configuration
    cfg = pixivtools.load_pixiv_config("config.yaml")
    service = pixivtools.new_pixiv_service(cfg)
    crawler = service.crawler()
    
    # Example crawling tasks
    # 1. Get monthly ranking for specific date
    crawler.get_by_rank(pixivtools.RankType.MONTHLY, 20250313, 1)
    
    # 2. Get recommended artworks
    crawler.get_by_recommend()
    
    # 3. Get artworks from pixivision
    crawler.get_by_pixivision_aid(9374)
    
    # 4. Get similar artworks
    crawler.get_by_similar_artwork(115812789)

if __name__ == "__main__":
    run_config_file_example() 