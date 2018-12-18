from flask import current_app as app, jsonify, abort, request


def fetch_data(spider_name, url='/<spider_name>/fetch-data', methods=['GET']):
    print('At the specified endpoints...')
    return jsonify(message='Fetch Successful...' + spider_name), 200


def search(spider_name, search_params, url='/<spider_name>/search/<search_params>', methods=['GET']):
    print('Search params: ', search_params)
    return jsonify(message=search_params), 200
