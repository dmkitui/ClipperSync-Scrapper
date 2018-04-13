import os

SPIDER_SETTINGS = [
    {
        'endpoint': 'clippersync',
        'location': 'spiders.ClippersyncSpider',
        'spider': 'ClippersyncSpider',
        'email': os.environ.get('CLIPPER_EMAIL'),
        'password': os.environ.get('CLIPPER_PASSWORD'),
        'scrapy_settings': {
            'ITEM_PIPELINES': {
                'pipelines.AddTablePipeline': 500
            },
            'USER_AGENT': 'Alphadog'
        }
    }
]
