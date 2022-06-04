def my_jwt_response_payload_handler(token, user=None, request=None, role=None):
    if user.is_authenticated:
        data = {"code": 20000,
                "message": "success",
                "data": {
                    # 'auth': True,
                    'id': user.id,
                    'name': user.username,
                    # 'role': role,
                    # 'email': users.email,
                    'token': token,
                }
                }
    else:
        data = {
            "code": 401,
            "message": "用户不存在或无权限",
            "data": {}
        }
    return data
