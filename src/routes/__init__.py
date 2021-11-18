from sanic import Blueprint
from .vpn_user import vpnuser
from .session import session

routes = Blueprint.group([vpnuser, session], url_prefix='/app')


