#!/usr/bin/python
# coding=utf-8
import paramiko
def remote_exec(ip,username,passwd,exe_command):
    try:
        port = "22"
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(ip, port, username, passwd)
        stdin, stdout, sterr = s.exec_command(exe_command)
    except Exception as e:
        result = {'status': "1", 'info':"link fault"}
    else:
        result = {'status': "0", 'info': stdout.read().rstrip()}
    s.close()
    return result

def remote_put(ip,username,passwd,local_path,remote_path):
    try:
        t = paramiko.Transport((ip, 22))
        t.connect(username=username, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, remote_path)
        t.close()
    except Exception, e:
        result = {'status': "1", 'info': "push fault"}
    else:
        result = {'status': "0", 'info': "sucessful"}
    t.close()
    return result
