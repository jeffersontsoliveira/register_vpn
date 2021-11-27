from src.models.vpn_user import UserVPN
from sanic import response
from sanic import Request
from src.database.database import connection
from datetime import datetime
from src.utils.serialize import Serialize
# from src.controllers.authorization import authorized
import json


class UserVPNController:
    @staticmethod
    async def index(request: Request):
        page = 1
        size = 5
        sizes = [5, 10, 20]

        if 'page' in request.args:
            _page: str = request.args['page'][0]
            if not _page.isnumeric():
                return response.json({'pages': 'arguments page must be numeric'}, status=400)

            page: int = int(_page)

        if 'size' in request.args:
            _size: str = request.args['size'][0]

            if not _size.isnumeric():
                return response.json({'size': 'argument size must be numeric'}, status=400)

            _size: int = int(_size)
            if _size in sizes:
                size = _size

        users = []
        query = UserVPN.select()

        count = query.count()
        print(f'count: {count}')
        pages = (count // size) + 1 if (count % size) > 0 else 0

        query = query.paginate(page=page, paginate_by=size)

        for user in query:
            users.append(user.json)

        data = dict()
        data['pages'] = pages
        data['users'] = users

        return response.json(data, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def show(request: Request, id_user):
        user = UserVPN.get_or_none(id=id_user)

        if user.json['admin'] is True:
            return response.json({'user': 'user not found'}, status=404)

        return response.json(user.json, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def store(request: Request):
        uid = request.headers['user']
        user = UserVPN.get_or_none(id=uid).json
        print(user)
        if user['admin'] is True:
            with connection.atomic() as transaction:
                data = request.json
                # data['filename'] =

                errors = UserVPN.validate(**data)

                if bool(errors):
                    return response.json(errors, status=400)

                user: UserVPN = UserVPN.create(**data)
                user_dict: dict = user.json
                user_dict['filename'] = f'http://0.0.0.0:3000/files/{user.filename}'

                return response.json(user, status=201, dumps=json.dumps, cls=Serialize)
        else:
            return response.json({'user': 'user has no permission'}, status=401)

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
