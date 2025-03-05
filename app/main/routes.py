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
        if request.headers.get('Content-Type') != 'application/json':
            #print(request.form, flush=True)
            #tags = print(request.form.get('To', ''), flush=True) # remove @.*, split by @ into list
            for key in request.files:
                #if request.files[key].mimetype in ['application/pdf']:
                print(dir(request.files[key]), flush=True)
                print(request.files[key].mimetype, flush=True)
                attachment = request.files[key]
                file_content = attachment.read()
                file_dir = os.environ.get('FILE_DIR', '/tmp')
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                with open(f'{file_dir}/{attachment.filename}', 'wb') as file:  # pylint:disable=unspecified-encoding
                    file.write(file_content)
                print(f'file saved to {file_dir}/{attachment.filename}.log', flush=True)
            ## Print or log attachments
            return jsonify({'status': 'invalid content type'}), 200
        publish.single(
            request.json.get('topic'),
            request.data,
            hostname=os.environ.get('MQTT_HOST', 'localhost'),
            port=int(os.environ.get('MQTT_PORT', '1883'))
        )
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'unauthorized'}), 401
