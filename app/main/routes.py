""" all routes will end up here or loaded here for flask """
# pylint:disable=cyclic-import
import os

from flask import jsonify, request
from paho.mqtt import publish

from app.main import BP as blueprint


@blueprint.route('/', methods=['POST'])
def main_route():
    """ Main route """
    if request.headers.get('Authorization') == f'Bearer {os.environ.get("API_KEY")}':
        print(request.data)
        publish.single(
            request.json['topic'],
            request.data,
            hostname=os.environ.get('MQTT_HOST', 'localhost'),
            port=int(os.environ.get('MQTT_PORT', '1883'))
        )
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'unauthorized'}), 401
