import os

SPIDER_SETTINGS = [
    {
        'endpoint': 'clippersync',
        'location': 'spiders.ClippersyncSpider',
        'spider': 'ClippersyncSpider',
        'email': os.environ.get('CLIPPER_EMAIL'),
        'password': os.environ.get('CLIPPER_PASSWORD'),
        'database': {
            'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'cybertron',
            'password': 'root',
            'database': os.environ.get('CLIPPER_DB_NAME') # 'clipper_raw_data'
        },
        'scrapy_settings': {
            'ITEM_PIPELINES': {
                'app.pipelines.AddTablePipeline': 500
            }
        }
    }
]
