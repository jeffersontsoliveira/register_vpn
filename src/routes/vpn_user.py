from src.controllers.vpn_user import UserVPNController
from sanic import Blueprint
from sanic.request import Request
from src.controllers.authorization import app_authorization

vpnuser = Blueprint('content_user', url_prefix='/vpnusers')

decorators = app_authorization()


@vpnuser.get('/')
@app_authorization()
async def index(request: Request):
    return await UserVPNController.index(request)


@vpnuser.get('/<id_user:int>')
@app_authorization()
async def show(request: Request, id_user):
    return await UserVPNController.show(request, id_user)


@vpnuser.post('/')
@app_authorization()
async def store(request: Request):
    return await UserVPNController.store(request)


@vpnuser.delete('/<id_user:int>')
@app_authorization()
async def remove(request: Request, id_user):
    return await UserVPNController.remove(request, id_user)


@vpnuser.put('/<id_user:int>')
@app_authorization()
async def update(request: Request, id_user):
    return await UserVPNController.update(request, id_user)

