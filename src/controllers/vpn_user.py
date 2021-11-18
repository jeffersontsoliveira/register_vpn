from src.models.vpn_user import UserVPN
from sanic import response
from sanic import Request
from src.database.database import connection
from datetime import datetime
from src.utils.serialize import Serialize
import json


class UserVPNController:
    @staticmethod
    async def index(request: Request):
        pass

    @staticmethod
    async def show(request: Request, id_user):
        user = UserVPN.get_or_none(id=id_user)

        if user is None:
            return response.json({'user': 'user not found'}, status=404)

        return response.json(user.json, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def store(request: Request):
        with connection.atomic() as transaction:
            data = request.json

            errors = UserVPN.validate(**data)

            if bool(errors):
                return response.json(errors, status=400)

            user: UserVPN = UserVPN.create(**data)

            return response.json(user.json, status=201, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def update(request: Request, id_user):
        user = UserVPN.get_or_none(id=id_user)

        if user is None:
            return response.json({'user': 'user not found '}, status=404)

        data = request.json.copy()

        user_dict = user.json
        user_dict.update(data)

        errors = UserVPN.validate(**user_dict)

        if bool(errors):
            return response.json(errors, status=400)

        user_dict['updatedAt'] = datetime.utcnow()

        UserVPN.update(**user_dict).where(UserVPN.id == user.id).execute()

        return response.json(user_dict, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def remove(request: Request, id_user):
        user = UserVPN.get_or_none(id=id_user)

        if user is None:
            return response.json({'user': 'user not found'}, status=404)

        user.delete_instance(recursive=True)

        return response.empty()
