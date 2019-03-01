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
    args = ['pip', 'install', '-U', '-r', cd.as_posix() + '/requirements.txt', '--target', '.']
    subprocess.call(args)
    username = os.getenv('USERNAME', '')
    src = cd / (username + '.json')
    copy = cd / 'gspread.json'
    shutil.copyfile(src, copy)
    pack = Path(shutil.make_archive((cd.parent / 'enterlist').as_posix(), 'zip'))
    os.chdir(cd.parent)
    args = ['aws', 's3', 'cp', pack.name, 's3://' + os.getenv('S3_BUCKET') + '/' + pack.name, '--profile', username]
    subprocess.call(args)
    return cd.parent


def create():
    username = os.getenv('USERNAME', '')
    os.chdir(deploy())
    args = ['aws', 'lambda', 'create-function', '--cli-input-json', 'file://settings/aws_caller_' + username + '.json',
            '--profile', username]
    subprocess.call(args)
    args = ['aws', 'lambda', 'create-function', '--cli-input-json', 'file://settings/aws_sender_' + username + '.json',
            '--profile', username]
    subprocess.call(args)
    print("finish")


def update():
    username = os.getenv('USERNAME', '')
    os.chdir(deploy())
    args = ['aws', 'lambda', 'update-function-code', '--cli-input-json',
            'file://settings/aws_caller_update_' + username + '.json', '--profile',
            username]
    subprocess.call(args)
    args = ['aws', 'lambda', 'update-function-code', '--cli-input-json',
            'file://settings/aws_sender_update_' + username + '.json', '--profile',
            username]
    subprocess.call(args)
    print("finish")


def main():
    # create()
    update()


if __name__ == '__main__':
    main()
