import uuid

from api.lib.common_setting.utils import get_cur_time_str


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_new_file_name(name):
    ext = name.split('.')[-1]
    prev_name = ''.join(name.split(f".{ext}")[:-1])
    uid = str(uuid.uuid4())
    cur_str = get_cur_time_str('_')
    return f"{prev_name}_{cur_str}_{uid}.{ext}"
