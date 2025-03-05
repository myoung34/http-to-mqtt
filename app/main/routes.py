""" all routes will end up here or loaded here for flask """
# pylint:disable=cyclic-import
import os

import requests
from flask import jsonify, request

from app.main import BP as blueprint


@blueprint.route('/', methods=['POST'])
def main_route():
    """ Main route """
    api_key = request.headers.get('Authorization', request.args.get('api_key'))
    if api_key == f'Bearer {os.environ.get("API_KEY", '')}' or api_key == os.environ.get('API_KEY', ''): # pylint:disable=line-too-long
        if request.headers.get('Content-Type') != 'application/json':
            #tags = print(request.form.get('To', ''), flush=True) # remove @.*, split by @ into list
            for key in request.files:
                if request.files[key].mimetype not in ['application/pdf', 'image/jpeg']:
                    return jsonify({f'invalid content type: {request.files[key].mimetype}'}), 400

                attachment = request.files[key]
                file_content = attachment.read()
                file_dir = os.environ.get('FILE_DIR', '/tmp')
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                with open(f'{file_dir}/{attachment.filename}', 'wb') as file:  # pylint:disable=unspecified-encoding
                    file.write(file_content)
                ## if its an image convert to PDF
                #if request.files[key].mimetype == 'image/jpeg':
                #    image = Image.open(request.files[key])
                #    image.show()
                #    pdf_path = "/tmp/test.pdf"

                #    images[0].save(
                #        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
                #    )
                print(f'file saved to {file_dir}/{attachment.filename}', flush=True)
                resp = requests.post(
                    f'{os.environ.get('PAPERLESS_URL')}/api/documents/post_document/',
                    files={'file': open(f'{file_dir}/{attachment.filename}', 'rb')}, # pylint:disable=consider-using-with
                    headers={'Authorization': f'Token {os.environ.get("PAPERLESS_API_KEY")}'},
                    timeout=90, # they can be large
                )
                # resp is just a quoted string
                print(f'... id ....{resp.text}', flush=True)

            ## Print or log attachments
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'unauthorized'}), 401
