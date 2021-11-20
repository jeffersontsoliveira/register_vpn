from functools import wraps
from sanic.response import json
from src.models import UserVPN
from sanic.request import Request
from sanic import response

import jwt

# def authorized(methods=['GET', 'PUT', 'POST', 'DELETE']):
#     def decorator(f):
#         @wraps(f)
#         async def decorated_function(request, *args, **kwargs):
#             request.headers['user'] = UserVPN.id
#             if request.method not in methods:
#                 response = await f(request, *args, **kwargs)
#                 return response
#             if request.token:
#                 token = request.token
#                 user_id = await request authorization('TOKEN:{}'.format(token))
#                 if user_id:
#                     response = await f(request, *args, **kwargs)
#                     return response
#             return json({}, 403)
#         return decorated_function
#     return decorator


def app_authorization():
    def decorator(func):
        @wraps(func)
        async def authorization(request: Request, *args, **kwargs):
            if request.token is None:
                return response.json({'token': 'token not provider'}, status=401)
            token = request.token
            secret = '5ba4919543f7d155c9838c20499e30c7'

            try:
                token_decoded = jwt.decode(
                    token,
                    secret,
                    algorithms=['HS256']
                )

            except jwt.ExpiredSignatureError:
                return response.json({'token': 'token expired'}, status=403)

            except jwt.InvalidTokenError:
                return response.json({'token': 'token invalid'}, status=403)

            uid = token_decoded['user']
            user = UserVPN.get_or_none(id=uid)

            if user is None:
                return response.json({'token': 'token invalid'}, status=403)

            request.headers['user'] = user.id

            return await func(request, *args, **kwargs)

        return authorization

    return decorator
