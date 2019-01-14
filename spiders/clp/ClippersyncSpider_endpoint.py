import pymongo
from flask import request
from flask import current_app as app, jsonify


# TODO Add Cache


def fetch_data(spider_name, url='/<spider_name>/fetch-data', methods=['GET']):
    """
    Endpoint to fetch all data from db
    :param spider_name: name of the spider
    :param url: URL of the endpoint.
    :param methods: GET.
    :return: all items
    """
    db_settings = {}
    for spider in app.config['SPIDER_SETTINGS']:
        if spider_name == spider['endpoint']:
            db_settings = spider['database']
            break

    if not db_settings:
        return jsonify(message='The specified spider does not exist')

    client = pymongo.MongoClient(db_settings['MONGO_URI'])
    db = client[db_settings['MONGO_DB']]
    items = db[db_settings['COLLECTION_NAME']]
    cursor_object = items.find({}).sort('date', pymongo.DESCENDING)

    results = []
    for result in cursor_object:
        result.update({'_id': str(result['_id'])})
        results.append(result)

    return jsonify(message=results), 200


def search(spider_name, url='/<spider_name>/search/', methods=['GET']):
    """
    Endpoint to perform search.
    :param spider_name: Name of the spider to run
    :param url: URL of the endpoint. It should have a search parameter in the format ?q=
    :param methods: GET
    :return: items matching the search parameters
    """
    db_settings = {}
    search_terms = request.args.get('q', '')

    for spider in app.config['SPIDER_SETTINGS']:
        if spider_name == spider['endpoint']:
            db_settings = spider['database']
            break

    if not db_settings:
        return jsonify(message='The specified spider does not exist')

    client = pymongo.MongoClient(db_settings['MONGO_URI'])
    db = client[db_settings['MONGO_DB']]
    items = db[db_settings['COLLECTION_NAME']]
    cursor_object = items.find({'$text': {'$search': search_terms}}).sort('date')

    results = []
    for result in cursor_object:
        result.update({'_id': str(result['_id'])})
        results.append(result)

    return jsonify(message=results), 200
