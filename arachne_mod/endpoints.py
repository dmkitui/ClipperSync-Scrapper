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
    engine = db_connect()
    create_clipperdata_table(engine)
    session = sessionmaker(bind=engine)()
    # session = Session()
    data = session.query(ClipperData).order_by(desc('date')).all()
    session.close()

    raw_data = [d.__dict__ for d in data]
    output = [{'id':x['id'], 'date': x['date'], 'note': x['note']} for x in raw_data]

    return jsonify(message='what....', data=output), 200
