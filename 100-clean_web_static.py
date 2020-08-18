#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.api import *
from fabric.operations import put, run, sudo
import os
from fabric.api import run, local, sudo, env
from datetime import datetime


dt = datetime.now()

env.hosts = ['34.74.35.201', '35.196.181.73']
env.user = 'ubuntu'


def do_pack():
    """ Packs web_static files into .tgz file
    """
    file_name = 'versions/web_static_{}{}{}{}{}{}.tgz'.format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    local('mkdir -p versions')
    command = local("tar -cvzf " + file_name + " ./web_static/")
    if command == 0:
        return file_name
    return None


def do_deploy(archive_path):
    """ deploy an archive from the archive_path
    """
    if os.path.exists(archive_path) is False:
        return False
    file_name = os.path.splitext(os.path.split(archive_path)[1])[0]
    target = '/data/web_static/releases/' + file_name
    path = archive_path.split('/')[1]
    try:
        """put("{}/tmp/".format(archive_path))
        run('sudo mkdir -p {}'.format(target))
        run('sudo tar -xzf /tmp/{} -C {}/'.format(path, target))
        run('sudo rm /tmp/{}'.format(path))
        run('sudo mv {}/web_static/* {}/'.format(target, target))
        run('sudo rm -rf {}/web_static'.format(target))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}/ /data/web_static/current'.format(target))"""

        put(archive_path, "/tmp/")
        run('sudo mkdir -p ' + target)
        run('sudo tar -xzf /tmp/' + path + ' -C ' + target + '/')
        run('sudo rm /tmp/' + path)
        run('sudo mv ' + target + '/web_static/* ' + target + '/')
        run('sudo rm -rf ' + target + '/web_static')
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s ' + target + '/ /data/web_static/current')
        return True
    except:
        return False


def deploy():
    """ make and ship static
    """
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)


def do_clean(number=0):
    """ Deletes out-of-date archives. Cleans old archives
    """
    number = int(number)
    with lcd('versions'):
        if number == 0 or number == 1:
            local('ls -t | tail -n +2 | xargs rm -rfv')
        else:
            local('ls -t | tail -n +{} | xargs rm -rfv'.format(number + 1))
    with cd('/data/web_static/releases/'):
        if number == 0 or number == 1:
            run('ls -t | tail -n +2 | xargs rm -rfv')
        else:
            run('ls -t | tail -n +{} | xargs rm -rfv'.format(number + 1))
