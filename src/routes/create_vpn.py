from src.controllers.create_vpn import VPNController
from sanic import Blueprint
from sanic.request import Request
from src.controllers.authorization import app_authorization

createvpnuser = Blueprint('content_user', url_prefix='/createvpnuser')

decorators = app_authorization()


@createvpnuser.post('/')
@app_authorization()
async def create_user_vpn(request: Request, id_user):
    return await VPNController.create_user_vpn(request, id_user)


@createvpnuser.get('/<id_user:int>')
@app_authorization()
async def download_vpn_user(request: Request, id_user):
    return await VPNController.download_vpn_user(request, id_user)
