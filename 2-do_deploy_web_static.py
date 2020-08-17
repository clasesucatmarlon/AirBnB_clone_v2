#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.operations import put, run, sudo
from os.path import exists
from fabric.api import *
from datetime import datetime


dt = datetime.now()

env.hosts = ['34.74.35.201', '35.196.181.73']


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
    if exists(archive_path) is False:
        return False
    else:
        pass
    try:
        put(archive_path, "/tmp/")
        fil = archive_path.split("/")[1].split(".")[0]
        path = "/data/web_static/releases/{}".format(fil)
        run("mkdir {}".format(path))
        run("tar -zxvf /tmp/{}.tgz -C {}/".format(fil, path))
        run("sudo rm /tmp/{}".format(archive_path.split("/")[1]))
        run("sudo rm /data/web_static/current")
        run("sudo ln - sf / data/web_static/releases/{}\
            / data/web_static/current".format(fil))
        run("sudo mv / data/web_static/releases/{}/web_static/*\
        / data/web_static/releases/{}".format(fil, fil))
        run("rm -rf /data/web_static/releases/{}/web_static/".format(fil))
        return True
    except:
        return False
