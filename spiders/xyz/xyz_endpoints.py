from flask import current_app as app, jsonify, abort, request


def fetch_data_xyz(spider_name, url='/<spider_name>/fetch-data-xyz', methods=['GET']):
    return jsonify(message='Fetch Successful...' + spider_name), 200
# 
# def fat():
#     return jsonify(message='what?'), 400