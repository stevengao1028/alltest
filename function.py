#!/usr/bin/python
# coding=utf-8
#0:ok,1:args or commands error,2:link fault
import paramiko
import commands
def remote_exec(ip,username,passwd,exe_command):
    try:
        port = "22"
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(ip, port, username, passwd)
        stdin, stdout, stderr = s.exec_command(exe_command)
    except Exception, e:
        result = {'status': "2", 'info':e}
    else:
        err_list = stderr.readlines()
        if len(err_list) >0:
            result = {'status': "1", 'info': err_list[0]}
        else:
            result = {'status': "0", 'info': stdout.read().rstrip()}
    s.close()
    return result

def remote_sftp(ip,action,username,passwd,local_path,remote_path):
    try:
        t = paramiko.Transport((ip, 22))
        t.connect(username=username, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        if action =="put":
            sftp.put(local_path, remote_path)
        elif action =="get":
            sftp.get(remote_path, local_path)
    except Exception, e:
        result = {'status': "1", 'info': "faild"}
    else:
        result = {'status': "0", 'info': "sucessful"}
    t.close()
    return result

#exe_command
def exe_command(ip,exe_cmd):
    if ip == "127.0.0.1":
        (status,output)=commands.getstatusoutput(exe_cmd)
        result={'status':str(status),'info':output}
        return result
    else:
        username= "root"
        passwd="abc,123"
        result=remote_exec(ip,username,passwd,exe_cmd)
        return result
#init disk
def disk_init(disk=""):
    exe_cmd="dd if=/dev/zero of="+disk+" bs=512 count=1000"
    (status, output) = commands.getstatusoutput(exe_cmd)
    result = {'status': str(status), 'info': output}
    return result

