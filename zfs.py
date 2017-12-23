#!/usr/bin/python
# coding=utf-8
import commands,json
from function import *

class zfs():
    def __init__(self,ip="127.0.0.1",pool_name="",raid="0",disks=[],spares=[],old_disk="",new_disk="",state=""):
        self.ip=ip
        self.pool_name=pool_name
        self.raid=raid
        self.disks=disks
        self.sapres=spares
        self.old_disk=old_disk
        self.new_disk=new_disk
        self.state=state
    #exe_command
    def exe_command(self,exe_cmd):
        if self.ip == "127.0.0.1":
            (status,output)=commands.getstatusoutput(exe_cmd)
            result={'status':str(status),'info':output}
            return result
        else:
            username= "root"
            passwd="abc,123"
            result=remote_exec(self.ip,username,passwd,exe_cmd)
            return result


    #pre-check system mod
    def check_mod(self):
        (status,output)=commands.getstatusoutput('zpool status')
        if status != 0:
            exe_cmd="modprobe zfs"
            result=self.exe_command(exe_cmd)
            return result
        else:
            result={'status':str(status),'info':output}
            return result

    #query_zpool
    def zpool_query(self):
        pool_name = self.pool_name
        exe_cmd = "zpool status "+pool_name
        result = self.exe_command(exe_cmd)
        pool_list =[]
        for pool in result['info'].split('errors'):
            pool_info = {'name':'','state':'','disks':'','spares':'','raid':'0'}
            disks=[]
            spares=[]
            for line in pool.split('\n'):
                if line and 'config' not in line and 'spares' not in line:
                    item = line.lstrip(r'       ').split()[0]
                    value = line.lstrip(r'      ').split()[1]
                    if item =='pool:':
                        pool_info['name'] = value
                    if item =='state:':
                        pool_info['state'] = value
                    if item.startswith('sd') and value !="AVAIL":
                        disks.append(item)
                        pool_info['disks'] = disks
                    if value =="AVAIL":
                        spares.append(item)
                        pool_info['spares'] = spares
                    if  item.startswith('raidz1'):
                        pool_info['raid'] = "5"
                    if  item.startswith('raidz2'):
                        pool_info['raid'] = "6"
            if pool_info['name']:
                pool_list.append(pool_info)
        result = pool_list
        # exe_cmd="zpool status "+pool_name+"""  2>/dev/null|awk -F" " '$1~/^pool:/{name=$2}$1~/^sd/{rdisk["\\"",$1,"\\""]=$2}$1~/errors:/{printf "{\\"name\\":\\""name"\\",";for (i in rdisk){printf i":\\""rdisk[i]"\\","}{printf "},"}}END{print ""}'|sed 's/,}/}/g;s/,$//;s/^/[/;s/$/]/'"""
        # result=self.exe_command(exe_cmd)
        return result



    #add_zpool
    def zpool_add(self):
        pool_name=self.pool_name
        raid=self.raid
        disks=self.disks
        spares=self.sapres
        if pool_name == "":
            result={'status':"1",'info':"pool name can`t be null"}
            return result
        if raid == "5":
            raid_level="raidz1"
        elif raid == "6":
            raid_level="raidz2"
        elif raid == "0":
            raid_level=""
        else :
            result={'status':"1",'info':"raid level did not been define"}
            return result
        query_result=self.zpool_query()
        if query_result :
            result={'status':"1",'info':"pool is exsit"}
            return result
        elif disks :
            if spares:
                exe_cmd="zpool create "+pool_name+' '+raid_level+' '+' '.join(disks)+' spare '+' '.join(spares)+' -f'
            else:
                exe_cmd = "zpool create " + pool_name + ' ' + raid_level + ' ' + ' '.join(disks)+' -f'
            result=self.exe_command(exe_cmd)
            return result
        else:
            result={'status':"1",'info':"disk can`t be null"}
            return result

    #del_zpool
    def zpool_del(self):
        pool_name=self.pool_name
        if pool_name == "":
            result={'status':"1",'info':"pool name can`t be null"}
            return result
        query_result=self.zpool_query()
        if query_result :
            exe_cmd="zpool destroy "+pool_name
            result=self.exe_command(exe_cmd)
            return result
        else:
            result={'status':"1",'info':"pool isn`t exsit"}
            return result


    #replace
    def replace_disk(self):
        pool_name=self.pool_name
        old_disk=self.old_disk
        new_disk=self.new_disk
        if pool_name == "" or old_disk == "" or new_disk == "":
            result={'status':"1",'info':"pool name ,old disk or new disk can`t be null"}
            return result
        query_result=self.zpool_query(pool_name)
        if query_result :
            exe_cmd="zpool replace "+pool_name+' '+old_disk+' '+new_disk
            result=self.exe_command(exe_cmd)
            return result
        else:
            result={'status':"1",'info':"pool isn`t exsit"}
            return result

