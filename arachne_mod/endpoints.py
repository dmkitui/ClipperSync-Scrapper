import json
from arachne_mod import database_operations
from flask import current_app as app, jsonify, abort, request
from arachne_mod.scrapy_utils import start_crawler
from models import ClipperData, db_connect, create_clipperdata_table
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import loads, dumps


def list_spiders_endpoint():
    """It returns a list of spiders available in the SPIDER_SETTINGS dict

    .. version 0.4.0:
        endpoint returns the spidername and endpoint to run the spider from
    """
    spiders = {}
    for item in app.config['SPIDER_SETTINGS']:
        spiders[item['endpoint']] = request.url_root + 'run-spider/' + item['endpoint']
    return jsonify(endpoints=spiders)


def run_spider_endpoint(spider_name):
    """Search for the spider_name in the SPIDER_SETTINGS dict and
    start running the spider with the Scrapy API

    .. version 0.4.0:
        endpoint returns the `status` as `running` and a way to go back to `home` endpoint
    """

    for item in app.config['SPIDER_SETTINGS']:
        if spider_name in item['endpoint']:
            spider_loc = '%s.%s' % (item['location'], item['spider'])
            start_crawler(spider_loc, app.config, item.get('scrapy_settings'))
            return jsonify(home=request.url_root, status='running', spider_name=spider_name)
    return abort(404)


def fetch_data(spider_name):
    """
    Endpoint to enable access to the scraped data
    :param spider_name: name of spider to fetch data
    :return: a json wiht the data
    """
    for item in app.config['SPIDER_SETTINGS']:
        if spider_name not in item['endpoint']:
            return jsonify(message='Invalid spider specified')

    output = database_operations.fetch_data()

    return jsonify(message='Fetch Successful...', data=output), 200


def edit_note(spider_name, note_id):

    request_data = json.loads(request.data.decode('utf-8'))
    print('Request body: ', request_data)

    for item in app.config['SPIDER_SETTINGS']:
        if spider_name not in item['endpoint']:
            return jsonify(message='Invalid spider specified')

    try:
        note_id = int(note_id)
    except Exception as e:
        return jsonify(message='Note ID should be an integer'), 400

    try:
        edited_note =request_data['edited_note']
    except IndexError:
        return jsonify(message='No Edits submitted')

    result, status_code = database_operations.edit_note(note_id, edited_note)

    if isinstance(result, str):
        return jsonify(message=result), status_code

    return jsonify(message='Edit Successful'), 201
