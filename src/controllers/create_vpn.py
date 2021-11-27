import subprocess
import sys
from src.models.vpn_user import UserVPN
from datetime import datetime

import hashlib
import aiofiles


class VPNController:
    @staticmethod
    async def create_user_vpn(request: Request):
        uid = request.headers['user']
        senha_sudo = 'lse'
        user = UserVPN.get_or_none(id=uid).json
        la = 'docker run -v OVPN_DATA:/etc/openvpn --rm -itd kylemanna/openvpn easyrsa build-client-full ' + user + ' nopass'
        subprocess.call('echo {} | sudo -S {}'.format(senha_sudo, la), shell=True)

    @staticmethod
    async def download_vpn_user(request: Request, id_user):
        uid = request.headers['user']
        seed = str(datetime.utcnow().timestamp())
        _hash = hashlib.md5(seed.encode()).hexdigest()

        user = UserVPN.get_or_none(id=uid).json
        path = f'./storage/{user}-{_hash}.ovpn'
        myoutput = open(path, 'w')

        args_2 = [
            'sudo',
            'docker',
            'run',
            '-v',
            'OVPN_DATA:/etc/openvpn',
            '--rm', 'kylemanna/openvpn',
            'ovpn_getclient',
            user]

        r = subprocess.run(args_2, stdout=myoutput, stderr=subprocess.PIPE, universal_newlines=True)
        r.stdout

        return f'{user}-{_hash}.ovpn'
