# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
from pathlib import Path


def deploy():
    """ Deploy package to AWS
    """
    cd = Path(__file__).parent
    os.chdir(cd)
    print(cd)
    args = ['pip', 'install', '-U', '-r', cd.as_posix() + '/requirements.txt', '--target', 'enterlist']
    subprocess.call(args)
    pack = Path(shutil.make_archive((cd.parent / 'enterlist').as_posix(), 'zip'))
    os.chdir(cd.parent)
    args = ['aws', 's3', 'cp', pack.name, 's3://' + os.getenv('S3_BUCKET') + '/' + pack.name]
    subprocess.call(args)
    return cd.parent


def create():
    os.chdir(deploy())
    args = ['aws', 'lambda', 'create-function', '--cli-input-json', 'file://aws_caller.json']
    subprocess.call(args)
    args = ['aws', 'lambda', 'create-function', '--cli-input-json', 'file://aws_sender.json']
    subprocess.call(args)
    print("finish")


def update():
    os.chdir(deploy())
    args = ['aws', 'lambda', 'update-function-code', '--cli-input-json', 'file://aws_sender_update.json']
    subprocess.call(args)
    args = ['aws', 'lambda', 'update-function-code', '--cli-input-json', 'file://aws_caller_update.json']
    subprocess.call(args)


if __name__ == '__main__':
    # update()
    create()
