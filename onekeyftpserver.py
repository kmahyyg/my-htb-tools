#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import sys

from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
import argparse
import os
import logging
import pathlib

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description="Onekey FTP Server brought to you by Patrick Young.")
parser.add_argument("-a", "--anonymous", help="Enable Anonymous Login, Default: True", action='store_true', default=True)
parser.add_argument("-u", "--username", help="Administrator Username", type=str, required=True)
parser.add_argument("-p", "--password", help="Administrator Password", type=str, required=True)
parser.add_argument("-P", "--port", help="Listen Port, Default: 21", type=int, default=21)
parser.add_argument("-c", "--cwd", help="FTP ROOT, Default: current folder", type=str, default=os.getcwd())


def premain():
    runargs = parser.parse_args()
    creds = []
    if os.path.isfile("recorded-ftp.log"):
        with open("recorded-ftp.log", "r") as credslog:
            data = credslog.readlines()
            for i in data:
                usr = i.strip().split("|")[1].strip().replace("\n", "").split(":")
                creds.append(usr)
    else:
        pass
    res = (creds, runargs)
    return res


def main(res):
    creds = res[0]
    runargs = res[1]
    if runargs.port == 21:
        if os.getuid() != 0:
            parser.print_help(sys.stderr)
            raise OSError("Bind Port 21 Need Root privileges.")
    if runargs.cwd:
        servroot = str(pathlib.Path(runargs.cwd).resolve())
    authorization = DummyAuthorizer()
    if runargs.username and runargs.password:
        authorization.add_user(runargs.username, runargs.password, homedir=servroot, perm="elradfmwMT")
    if runargs.anonymous:
        authorization.add_anonymous(homedir=servroot, perm="elrmwM")
    if len(creds) > 0:
        for i in creds:
            authorization.add_user(i[0], i[1], homedir=servroot, perm="elradfmwMT")
    hand = FTPHandler
    hand.authorizer = authorization
    hand.banner = "Welcome To My FTP"
    address = ('', runargs.port)
    server = FTPServer(address, hand)
    server.max_cons = 15
    server.max_cons_per_ip = 5
    server.set_reuse_addr()
    server.serve_forever()


if __name__ == '__main__':
    res = premain()
    main(res)
