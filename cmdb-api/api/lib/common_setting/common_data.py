import copy
import json

from flask import abort, current_app
from ldap3 import Connection
from ldap3 import Server
from ldap3.core.exceptions import LDAPBindError, LDAPSocketOpenError
from ldap3 import AUTO_BIND_NO_TLS

from api.extensions import db
from api.lib.common_setting.resp_format import ErrFormat
from api.models.common_setting import CommonData
from api.lib.utils import AESCrypto
from api.lib.common_setting.const import AuthCommonConfig, AuthenticateType, AuthCommonConfigAutoRedirect


class CommonDataCRUD(object):

    @staticmethod
    def get_data_by_type(data_type):
        CommonDataCRUD.check_auth_type(data_type)
        return CommonData.get_by(data_type=data_type)

    @staticmethod
    def get_data_by_id(_id, to_dict=True):
        return CommonData.get_by(first=True, id=_id, to_dict=to_dict)

    @staticmethod
    def create_new_data(data_type, **kwargs):
        try:
            CommonDataCRUD.check_auth_type(data_type)
            return CommonData.create(data_type=data_type, **kwargs)
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    @staticmethod
    def update_data(_id, **kwargs):
        existed = CommonDataCRUD.get_data_by_id(_id, to_dict=False)
        if not existed:
            abort(404, ErrFormat.common_data_not_found.format(_id))
        try:
            CommonDataCRUD.check_auth_type(existed.data_type)
            return existed.update(**kwargs)
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    @staticmethod
    def delete(_id):
        existed = CommonDataCRUD.get_data_by_id(_id, to_dict=False)
        if not existed:
            abort(404, ErrFormat.common_data_not_found.format(_id))
        try:
            CommonDataCRUD.check_auth_type(existed.data_type)
            existed.soft_delete()
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    @staticmethod
    def check_auth_type(data_type):
        if data_type in list(AuthenticateType.all()) + [AuthCommonConfig]:
            abort(400, ErrFormat.common_data_not_support_auth_type.format(data_type))

    @staticmethod
    def set_auth_auto_redirect_enable(_value: int):
        existed = CommonData.get_by(first=True, data_type=AuthCommonConfig, to_dict=False)
        if not existed:
            CommonDataCRUD.create_new_data(AuthCommonConfig, data={AuthCommonConfigAutoRedirect: _value})
        else:
            data = existed.data
            data = copy.deepcopy(existed.data) if data else {}
            data[AuthCommonConfigAutoRedirect] = _value
            CommonDataCRUD.update_data(existed.id, data=data)
        return True

    @staticmethod
    def get_auth_auto_redirect_enable():
        existed = CommonData.get_by(first=True, data_type=AuthCommonConfig)
        if not existed:
            return 0
        data = existed.get('data', {})
        if not data:
            return 0
        return data.get(AuthCommonConfigAutoRedirect, 0)


class AuthenticateDataCRUD(object):
    common_type_list = [AuthCommonConfig]

    def __init__(self, _type):
        self._type = _type
        self.record = None
        self.decrypt_data = {}

    def get_support_type_list(self):
        return list(AuthenticateType.all()) + self.common_type_list

    def get(self):
        if not self.decrypt_data:
            self.decrypt_data = self.get_decrypt_data()

        return self.decrypt_data

    def get_by_key(self, _key):
        if not self.decrypt_data:
            self.decrypt_data = self.get_decrypt_data()

        return self.decrypt_data.get(_key, None)

    def get_record(self, to_dict=False) -> CommonData:
        return CommonData.get_by(first=True, data_type=self._type, to_dict=to_dict)

    def get_record_with_decrypt(self) -> dict:
        record = CommonData.get_by(first=True, data_type=self._type, to_dict=True)
        if not record:
            return {}
        data = self.get_decrypt_dict(record.get('data', ''))
        record['data'] = data
        return record

    def get_decrypt_dict(self, data):
        decrypt_str = self.decrypt(data)
        try:
            return json.loads(decrypt_str)
        except Exception as e:
            abort(400, str(e))

    def get_decrypt_data(self) -> dict:
        self.record = self.get_record()
        if not self.record:
            return self.get_from_config()
        return self.get_decrypt_dict(self.record.data)

    def get_from_config(self):
        return current_app.config.get(self._type, {})

    def check_by_type(self) -> None:
        existed = self.get_record()
        if existed:
            abort(400, ErrFormat.common_data_already_existed.format(self._type))

    def create(self, data) -> CommonData:
        self.check_by_type()
        encrypted_data = self.encrypt(data)
        try:
            return CommonData.create(data_type=self._type, data=encrypted_data)
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    def update_by_record(self, record, data) -> CommonData:
        encrypted_data = self.encrypt(data)
        try:
            return record.update(data=encrypted_data)
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    def update(self, _id, data) -> CommonData:
        existed = CommonData.get_by(first=True, to_dict=False, id=_id)
        if not existed:
            abort(404, ErrFormat.common_data_not_found.format(_id))

        return self.update_by_record(existed, data)

    @staticmethod
    def delete(_id) -> None:
        existed = CommonData.get_by(first=True, to_dict=False, id=_id)
        if not existed:
            abort(404, ErrFormat.common_data_not_found.format(_id))
        try:
            existed.soft_delete()
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    @staticmethod
    def encrypt(data) -> str:
        if type(data) is dict:
            try:
                data = json.dumps(data)
            except Exception as e:
                abort(400, str(e))
        return AESCrypto().encrypt(data)

    @staticmethod
    def decrypt(data) -> str:
        return AESCrypto().decrypt(data)

    @staticmethod
    def get_enable_list():
        all_records = CommonData.query.filter(
            CommonData.data_type.in_(AuthenticateType.all()),
            CommonData.deleted == 0
        ).all()
        enable_list = []
        for auth_type in AuthenticateType.all():
            record = list(filter(lambda x: x.data_type == auth_type, all_records))
            if not record:
                config = current_app.config.get(auth_type, None)
                if not config:
                    continue

                if config.get('enable', False):
                    enable_list.append(dict(
                        auth_type=auth_type,
                    ))

                continue

            try:
                decrypt_data = json.loads(AuthenticateDataCRUD.decrypt(record[0].data))
            except Exception as e:
                current_app.logger.error(e)
                continue

            if decrypt_data.get('enable', 0) == 1:
                enable_list.append(dict(
                    auth_type=auth_type,
                ))

        auth_auto_redirect = CommonDataCRUD.get_auth_auto_redirect_enable()

        return dict(
            enable_list=enable_list,
            auth_auto_redirect=auth_auto_redirect,
        )

    def test(self, data):
        type_lower = self._type.lower()
        func_name = f'test_{type_lower}'
        if hasattr(self, func_name):
            try:
                return getattr(self, f'test_{type_lower}')(data)
            except Exception as e:
                abort(400, str(e))
        abort(400, ErrFormat.not_support_test.format(self._type))

    @staticmethod
    def test_ldap(data):
        ldap_server = data.get('ldap_server')
        ldap_user_dn = data.get('ldap_user_dn', '{}')
        username = data.get('username', '')
        user = ldap_user_dn.format(username)
        password = data.get('password', '')

        server = Server(ldap_server, connect_timeout=2)

        try:
            Connection(server, user=user, password=password, auto_bind=AUTO_BIND_NO_TLS)
        except LDAPBindError:
            ldap_domain = data.get('ldap_domain')
            user_with_domain = f"{username}@{ldap_domain}"
            try:
                Connection(server, user=user_with_domain, password=password, auto_bind=AUTO_BIND_NO_TLS)
            except Exception as e:
                raise Exception(ErrFormat.ldap_test_unknown_error.format(str(e)))

        except LDAPSocketOpenError:
            raise Exception(ErrFormat.ldap_server_connect_timeout)

        except Exception as e:
            raise Exception(ErrFormat.ldap_test_unknown_error.format(str(e)))

        return True
