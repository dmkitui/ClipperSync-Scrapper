import pymongo
from flask import current_app as app, jsonify


def fetch_data(spider_name, url='/<spider_name>/fetch-data', methods=['GET']):
    db_settings = {}
    for spider in app.config['SPIDER_SETTINGS']:
        if spider_name == spider['endpoint']:
            db_settings = spider['database']
            break

    if not db_settings:
        return jsonify(message='The specified spider does not exist')

    client = pymongo.MongoClient(db_settings['MONGO_URI'])
    db = client[db_settings['MONGO_DB_NAME']]
    items = db['MONGO_ITEMS']
    cursor_object = items.find({}, {'_id': 0})

    results = []
    for result in cursor_object:
        results.append(result)

    return jsonify(message=results), 200


def search(spider_name, search_params, url='/<spider_name>/search/<search_params>', methods=['GET']):
    db_settings = {}
    for spider in app.config['SPIDER_SETTINGS']:
        if spider_name == spider['endpoint']:
            db_settings = spider['database']
            break

    if not db_settings:
        return jsonify(message='The specified spider does not exist')

    client = pymongo.MongoClient(db_settings['MONGO_URI'])
    db = client[db_settings['MONGO_DB_NAME']]
    items = db['MONGO_ITEMS']
    cursor_object = items.find({"$text": {"$search": search_params}}, {'_id': 0})

    results = []
    for result in cursor_object:
        results.append(result)

    return jsonify(message=results), 200
