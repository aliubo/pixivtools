import pixivtools

def run_batch_processing_example():
    """Example: Batch processing multiple tasks"""
    # Make sure you have config.yaml file with proper configuration
    cfg = pixivtools.load_pixiv_config("config.yaml")
    service = pixivtools.new_pixiv_service(cfg)
    crawler = service.crawler()
    
    # Batch process multiple artwork IDs
    artwork_ids = [98538269, 60155475, 62608184]
    for artwork_id in artwork_ids:
        crawler.get_by_artwork_id(artwork_id)
    
    # Batch process multiple user IDs
    user_ids = [212801, 490219]
    for user_id in user_ids:
        crawler.get_by_user_id(user_id)
        
    # Get artworks from multiple tags
    tags = ["ホロライブ", "原神", "FGO"]
    for tag in tags:
        crawler.get_by_tag_popular(tag)

if __name__ == "__main__":
    run_batch_processing_example() 