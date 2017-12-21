#!/usr/bin/python
# coding=utf-8
import paramiko
import json
def remote_exec(ip,username,passwd,exe_command):
    port = "22"
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, port, username, passwd)
    stdin, stdout, sterr = s.exec_command(exe_command)
    result = {'status': str(sterr), 'info': stdout.read()}
    result = json.dumps(result)
    return result



