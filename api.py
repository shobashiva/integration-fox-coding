from flask import Flask, request, make_response, send_file
import os
import pathlib

from werkzeug.utils import secure_filename


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/", methods=['GET', ])
    def hello():
        return "hello"

    @app.route("/file", methods=['POST', ])
    def file_endpoint():
        file = request.files['file']
        current_dir = pathlib.Path().resolve()
        save_path = os.path.join(
            current_dir,
            'uploads/',
            secure_filename(file.filename)  # file name will be altered
        )

        current_chunk = int(request.form['dzchunkindex'])

        if os.path.exists(save_path) and current_chunk == 0:
            return make_response(('File already exists', 400))

        try:
            with open(save_path, 'ab') as f:
                f.seek(int(request.form['dzchunkbyteoffset']))
                f.write(file.stream.read())
        except OSError:
            return make_response(
                ("Could not write the file to disk", 500))

        return make_response(('Uploaded Chunk', 200))

    @app.route("/file/<fname>", methods=['GET', ])
    def file_download(fname):
        current_dir = pathlib.Path().resolve()
        file_path = os.path.join(
            current_dir,
            'uploads/',
            fname
        )
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return make_response(('File does not exist', 400))

    return app
