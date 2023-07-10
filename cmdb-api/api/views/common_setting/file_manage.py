# -*- coding:utf-8 -*-
import os

from flask import request, abort, current_app, send_from_directory
from werkzeug.utils import secure_filename

from api.lib.common_setting.resp_format import ErrFormat
from api.lib.common_setting.upload_file import allowed_file, generate_new_file_name
from api.resource import APIView

prefix = '/file'

ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'csv'
}


class FileExtensionAllowView(APIView):
    url_prefix = (f'{prefix}/allow_extensions',)

    def get(self):
        extensions = current_app.config.get('ALLOWED_EXTENSIONS', ALLOWED_EXTENSIONS)
        extensions = list(extensions)
        return self.jsonify(extensions)


class GetFileView(APIView):
    url_prefix = (f'{prefix}/<string:_filename>',)

    def get(self, _filename):
        return send_from_directory(current_app.config['UPLOAD_DIRECTORY_FULL'], _filename, as_attachment=True)


class PostFileView(APIView):
    url_prefix = (f'{prefix}',)

    def post(self):
        # check if the post request has the file part
        if 'file' not in request.files:
            abort(400, ErrFormat.no_file_part)

        file = request.files['file']

        if not file:
            abort(400, ErrFormat.file_is_required)
        extension = file.mimetype.split('/')[-1]
        if file.filename == '':
            filename = f'.{extension}'
        else:
            if extension not in file.filename:
                filename = file.filename + f".{extension}"
            else:
                filename = file.filename

        if allowed_file(filename, current_app.config.get('ALLOWED_EXTENSIONS', ALLOWED_EXTENSIONS)):
            filename = generate_new_file_name(filename)
            filename = secure_filename(filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_DIRECTORY_FULL'], filename))

            return self.jsonify(file_name=filename)

        abort(400, 'Extension not allow')
