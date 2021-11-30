import subprocess
import sys
from src.models.vpn_user import UserVPN
from datetime import datetime
import os
import aiofiles

import hashlib
import aiofiles


# class VPNController:
#     @staticmethod
async def create_user_vpn(username: str):
    senha_sudo = 'lse'
    print('çsldmamaslçdsmdçasldmalçdmasçmldça')
    user = username
    print(user)
    la = 'docker run -v OVPN_DATA:/etc/openvpn --rm -itd kylemanna/openvpn easyrsa build-client-full ' + user + ' nopass'
    subprocess.call('echo {} | sudo -S {}'.format(senha_sudo, la), shell=True)

    print('simsismsimsismsimsismismsismsimsimsismi')


    seed = str(datetime.utcnow().timestamp())
    _hash = hashlib.md5(seed.encode()).hexdigest()


    path = f'./storage/{user}-{_hash}.ovpn'
    vpn_file = open(path, 'w')

    args_2 = [
        'sudo',
        'docker',
        'run',
        '-v',
        'OVPN_DATA:/etc/openvpn',
        '--rm', 'kylemanna/openvpn',
        'ovpn_getclient',
        user]

    r = subprocess.run(args_2, stdout=vpn_file, stderr=subprocess.PIPE, universal_newlines=True)

    # r.stdout

    return f'{user}-{_hash}.ovpn'
