#!/usr/bin/python3
"""that distributes an archive"""
from fabric.api import local, put, env, run
from datetime import datetime
from os import path

env.hosts = ['35.196.97.61', '34.75.200.40']


def do_pack():
    """contents of the web_static"""
    f = datetime.now()

    file_name = "web_static_{}{}{}{}{}{}.tgz".format(
        f.year, f.month, f.day, f.hour, f.minute, f.second)

    local('mkdir -p versions')
    result = local('tar -cvzf versions/{} web_static'.format(file_name))
    print("Packing web_static to versions/{}".format(file_name))

    if result == 0:
        return "versions/{}".format(file_name)
    return None


def do_deploy(archive_path):
    """Script distributes an archive"""
    if not path.exists(archive_path):
        return False

    try:
        archive_file = archive_path.split('/')[1]
        file_no_ext = archive_file.split('.')[0]
        releases = '/data/web_static/releases/versions/{}/'.format(file_no_ext)
        put(archive_path, '/tmp')
        run('sudo mkdir -p {}'.format(releases))
        run('sudo tar -xvf /tmp/{} -C {}'.format(archive_file, releases))
        run('sudo rm /tmp/{}'.format(archive_file))
        run('sudo mv {}/web_static/* {}'.format(releases, releases))
        run('sudo rm -rf {}/web_static'.format(releases))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(releases))
        return True
    except Exception as e:
        return False
