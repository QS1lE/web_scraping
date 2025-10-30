# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'stopgame_db'


BOT_NAME = 'stopgame_project'

SPIDER_MODULES = ['stopgame_project.spiders']
NEWSPIDER_MODULE = 'stopgame_project.spiders'

ROBOTSTXT_OBEY = False
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'INFO'

# Item Pipelines
ITEM_PIPELINES = {
    'stopgame_project.pipelines.MongoDBPipeline': 300,
}