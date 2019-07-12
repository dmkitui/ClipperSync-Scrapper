import pymongo
from flask import request
from flask import current_app as app, jsonify
from bson.objectid import ObjectId
from .helper_functions import db_connection


# TODO Add Cache


def fetch_data(spider_name, url='/<spider_name>/fetch-data', methods=['GET']):
    """
    Endpoint to fetch all data from db
    :param spider_name: name of the spider
    :param url: URL of the endpoint.
    :param methods: GET.
    :return: all items
    """
    all_spider_stats = db_connection(spider_name, 'stats')

    spider_stats = None
    for stat in all_spider_stats.find():
        if stat['spider_name'] == spider_name:
            spider_stats = stat['details']
            break

    print('Current Stats: ', spider_stats)

    items = db_connection(spider_name, 'items')

    if not isinstance(items, pymongo.collection.Collection):
        return items

    cursor_object = items.find({}, {'md5': False}).sort('date', pymongo.DESCENDING)

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

    search_terms = request.args.get('q', '')

    items = db_connection(spider_name, 'items')
    # items.create_index([('raw_note', pymongo.TEXT)], unique=True, background=True, sparse=True)

    if not isinstance(items, pymongo.collection.Collection):
        return items

    cursor_object = items.find({'$text': {'$search': str(search_terms)}}, {'md5': False}).sort('date', pymongo.DESCENDING)

    results = []
    for result in cursor_object:
        result.update({'_id': str(result['_id'])})
        results.append(result)

    return jsonify(message=results), 200


def fetch_one(spider_name, item_id, url='/<spider_name>/fetch-one/<item_id>', methods=['GET']):

    items = db_connection(spider_name, 'data')

    if not isinstance(items, pymongo.collection.Collection):
        return items

    cursor_object = items.find({"_id": ObjectId(item_id)})

    results = []
    for result in cursor_object:
        result.update({'_id': str(result['_id'])})
        results.append(result)

    if not results:
        return jsonify(message='Not Found'), 404

    return jsonify(message=results), 200
