# -*- coding:utf-8 -*-
from flask import request, abort, current_app
from werkzeug.utils import secure_filename
import lz4.frame
import magic

from api.lib.common_setting.const import MIMEExtMap
from api.lib.common_setting.resp_format import ErrFormat
from api.lib.common_setting.upload_file import allowed_file, generate_new_file_name, CommonFileCRUD
from api.resource import APIView

prefix = '/file'

ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'csv', 'svg'
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
        file_stream = CommonFileCRUD.get_file(_filename)
        return self.send_file(file_stream, as_attachment=True, download_name=_filename)


class PostFileView(APIView):
    url_prefix = (f'{prefix}',)

    def post(self):
        # check if the post request has the file part
        if 'file' not in request.files:
            abort(400, ErrFormat.no_file_part)

        file = request.files['file']

        if not file:
            abort(400, ErrFormat.file_is_required)

        m_type = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)

        if m_type == 'application/octet-stream':
            m_type = file.mimetype
        elif m_type == 'text/plain':
            # https://github.com/ahupp/python-magic/issues/193
            m_type = m_type if file.mimetype == m_type else file.mimetype

        extension = MIMEExtMap.get(m_type, None)

        if extension is None:
            abort(400, f"不支持的文件类型: {m_type}")

        filename = file.filename if file.filename and file.filename.endswith(extension) else file.filename + extension

        new_filename = generate_new_file_name(filename)
        new_filename = secure_filename(new_filename)
        file_content = file.read()
        compressed_data = lz4.frame.compress(file_content)
        try:
            CommonFileCRUD.add_file(
                origin_name=filename,
                file_name=new_filename,
                binary=compressed_data,
            )

            return self.jsonify(file_name=new_filename)
        except Exception as e:
            current_app.logger.error(e)
            abort(400, ErrFormat.upload_failed.format(e))
