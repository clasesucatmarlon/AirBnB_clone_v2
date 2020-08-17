#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.operations import put, run, sudo
import os
from fabric.api import run, local, sudo, env
from datetime import datetime


dt = datetime.now()

env.hosts = ['34.74.35.201', '35.196.181.73']


def do_pack():
    """compress + bundle local sweb files
    """
    try:
        if os.path.isdir("versions") is False:
            os.mkdir("versions")
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        packed = 'versions/web_static_' + time + '.tgz'
        fabric.api.local("tar -cvzf {} web_static".format(packed))
        return packed
    except:
        return None


def do_deploy(archive_path):
    """deploy an archive from the archive_path
    """
    if os.path.exists(archive_path) is False:
        return False
    file_name = os.path.splitext(os.path.split(archive_path)[1])[0]
    target = '/data/web_static/releases/' + file_name
    path = archive_path.split('/')[1]
    try:
        put(archive_path, "/tmp/")
        run('sudo mkdir -p ' + target)
        run('sudo tar -xzf /tmp/' + path + ' -C ' + target + '/')
        run('sudo rm /tmp/' + path)
        run('sudo mv ' + target + '/web_static/* ' + target + '/')
        run('sudo rm -rf ' + target + '/web_static')
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s ' + target + '/ /data/web_static/current')
        print('deploy success')
        return True
    except:
        return False
