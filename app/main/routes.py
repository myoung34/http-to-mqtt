""" all routes will end up here or loaded here for flask """
# pylint:disable=cyclic-import
import os

from flask import jsonify, request
from paho.mqtt import publish

from app.main import BP as blueprint


@blueprint.route('/', methods=['POST'])
def main_route():
    """ Main route """
    api_key = request.headers.get('Authorization', request.args.get('api_key'))
    if api_key == f'Bearer {os.environ.get("API_KEY", '')}' or api_key == os.environ.get('API_KEY', ''): # pylint:disable=line-too-long
        publish.single(
            request.json['topic'],
            request.data,
            hostname=os.environ.get('MQTT_HOST', 'localhost'),
            port=int(os.environ.get('MQTT_PORT', '1883'))
        )
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'unauthorized'}), 401
