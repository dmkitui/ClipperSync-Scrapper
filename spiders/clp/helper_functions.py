import pymongo
from flask import current_app as app, jsonify


def db_connection(spider_name, data):
    db_settings = {}
    for spider in app.config['SPIDER_SETTINGS']:
        if spider_name == spider['endpoint']:
            db_settings = spider['database']
            break

    if not db_settings:
        return jsonify(message='The specified spider does not exist'), 400

    client = pymongo.MongoClient(db_settings['MONGO_URI'])
    db = client[db_settings['MONGO_DB']]

    if data == 'items':
        return db[db_settings['CLIPPER_ITEMS']]
    elif data == 'stats':
        return db['spider_stats']
