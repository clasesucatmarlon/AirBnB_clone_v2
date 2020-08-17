#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.api import *
from fabric.operations import put, run
import time
import os
env.hosts = ['34.74.35.201', '35.196.181.73']


def do_deploy(archive_path):
    """ distributes archive to web servers
    """
    if os.path.isfile(archive_path) is False:
        return False

    full_filename = os.path.basename(archive_path)
    filename, ext = os.path.splitext(full_filename)
    dir_releases = "/data/web_static/releases"
    dir_current = "/data/web_static/current"
    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}/{}".format(dir_releases, filename))
        run("sudo tar -xzf /tmp/{} -C {}/{}".format(full_filename,
                                                    dir_releases,
                                                    filename))
        run("sudo rm /tmp/{}".format(full_filename))
        run("sudo mv {}/{}/web_static/* {}/{}".format(dir_releases, filename,
                                                      dir_releases, filename))
        run("sudo rm -rf {}/{}/web_static".format(dir_releases, filename))
        run("sudo rm -rf {}".format(dir_current))
        run("sudo ln -s {}/{}/ {}".format(dir_releases, filename, dir_current))
        return True
    except:
        return False
