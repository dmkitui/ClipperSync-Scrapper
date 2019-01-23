import os

SPIDER_SETTINGS = [
    {
        'endpoint': 'clippersync',
        'location': 'spiders.clp.ClippersyncSpider',
        'endpoint_location': 'spiders.clp.ClippersyncSpider_endpoint',
        'spider': 'ClippersyncSpider',
        'email': os.environ.get('CLIPPER_EMAIL'),
        'password': os.environ.get('CLIPPER_PASSWORD'),
        'database': {
            'MONGO_URI': os.environ.get('MONGO_URI'),
            'MONGO_DB': os.environ.get('MONGO_DB'),
            'RAW_COLLECTION_NAME': os.environ.get('RAW_COLLECTION_NAME'),
            'CLIPPER_ITEMS': os.environ.get('CLIPPER_ITEMS')
        },
        'scrapy_settings': {
            'ITEM_PIPELINES': {
                'app.pipelines.ProcessRawItem': 100
            }
        }
    },
    {
        'endpoint': 'xyz',
        'location': 'spiders.xyz.xyz',
        'endpoint_location': 'spiders.xyz.xyz_endpoints',
        'spider': 'xyz',
        'email': os.environ.get('CLIPPER_EMAIL'),
        'password': os.environ.get('CLIPPER_PASSWORD'),
        'database': {
            'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'cybertron',
            'password': 'root',
            'database': os.environ.get('CLIPPER_DB_NAME')
        },
        'scrapy_settings': {
            'ITEM_PIPELINES': {
                'app.pipelines.ProcessRawItem': 500
            }
        }
    }
]
