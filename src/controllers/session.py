import json
from sanic.request import Request
from sanic import response
from src.models.vpn_user import UserVPN
from datetime import datetime, timedelta
from src.utils.serialize import Serialize
import jwt


class SessionController:
    @staticmethod
    async def store(request: Request):
        name = request.json['username']
        password = request.json['password']

        user = UserVPN.get_or_none(username=name)
        if user is None:
            return response.json({'user': 'user not found'}, status=404)

        if user.password != password:
            return response.json({'password': 'password does not match'}, status=403)

        expired = datetime.utcnow() + timedelta(minutes=30)
        secret = 'b8019c5cd743abe5e568bca34e1035a2'

        payload ={
            'user': user.id,
            'exp': expired
        }
        token = jwt.encode(payload, secret, algorithm='HS256')

        data = dict()
        data['token'] = token
        data['user'] = user.json

        return response.json(data, dumps=json.dumps, cls=Serialize)
