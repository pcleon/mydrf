import uuid
from calendar import timegm
from datetime import datetime

from rest_framework_jwt.settings import api_settings

from users.serializers import MyUserSerializer
from rest_framework_jwt.compat import get_username
from rest_framework_jwt.compat import get_username_field

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

def my_jwt_response_payload_handler(token, user=None, request=None, role=None):
    myuser = MyUserSerializer(user).data
    if user.is_authenticated:
        data = {"code": 20000,
                "message": "success",
                "data": {
                    # 'auth': True,
                    # 'id': user.id,
                    # 'name': myuser['username'],
                    # 'roles': myuser['role_value'],
                    # 'email': users.email,
                    'token': token,
                }
                }

        return data


def my_jwt_payload_handler(user):
    username_field = get_username_field()
    username = get_username(user)

    payload = {
        'username': username,
    }
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload