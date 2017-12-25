#!/usr/bin/python
# coding=utf-8
from function import *
import re

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

    #pre-check system mod
    def check_mod(self):
        (status,output)=commands.getstatusoutput('zpool status')
        if status != 0:
            exe_cmd="modprobe zfs"
            exe_result=exe_command(self.ip,exe_cmd)
            result =exe_result
            return result
        else:
            result={'status':str(status),'info':output}
            return result

    #query_zpool
    def zpool_query(self):
        pool_name = self.pool_name
        exe_cmd = "zpool status "+pool_name
        exe_result = exe_command(self.ip,exe_cmd)
        pool_list =[]
        for pool in exe_result['info'].split('errors'):
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
        # exe_result=exe_command(self.ip,exe_cmd)
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
            exe_result=exe_command(self.ip,exe_cmd)
            result=exe_result
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
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
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
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
            return result
        else:
            result={'status':"1",'info':"pool isn`t exsit"}
            return result

class lvm():
    def __init__(self,ip="127.0.0.1",vg_name="",lv_name="",lv_size="",ex_size="",disk=[],old_disk=[],new_disk=[],state=""):
        self.ip = ip
        self.vg_name = vg_name
        self.lv_name = lv_name
        self.lv_size = lv_size
        self.ex_size = ex_size
        self.disks = disk
        self.old_disk = old_disk
        self.new_disk = new_disk
        self.state = state

    # def pv_query(self):
    #     exe_cmd="""pvs -o pv_name,pv_size,lv_name,lv_size,vg_size,vg_free,vg_name"""

    def pvl_info(self):
        exe_cmd = """pvs -o pv_name,vg_name,lv_name"""
        exe_result = exe_command(self.ip,exe_cmd)
        pvl = []
        if exe_result['status'] == "0":
            for list in exe_result['info'].split('\n'):
                if re.match(r'  /dev', list):
                    pv_info={'pv':"",'vg':"",'lv':""}
                    pv_info['pv'] = list.split()[0].split('/dev/')[1]
                    if len(list.split()) == 2:
                        pv_info['vg'] = list.split()[1]
                    if len(list.split()) == 3:
                        pv_info['lv'] = list.split()[2]
                    pvl.append(pv_info)
        result = pvl
        return result

    def pv_add(self):
        if self.new_disk:
            exe_cmd = "pvcreate  "+" ".join(self.new_disk)
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
        else:
                result = {'status': "1", 'info': "disk can`t be null"}
        return result

    def pv_remove(self):
        if  self.old_disk:
            exe_cmd = "pvremove  " +" ".join(self.old_disk)
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
        else:
            result = {'status': "1", 'info': "disk can`t be null"}
        return result

    def vg_add(self):
        query_result = self.pvl_info()
        if self.vg_name and self.disks:
            for pvl in query_result:
                if self.vg_name == pvl['vg'] :
                    result = {'status': "1", 'info': "vg group is exsit"}
                    return result
                exe_cmd = "vgcreate  " + self.vg_name +" "+" ".join(self.disks)
                exe_result = exe_command(self.ip, exe_cmd)
                result = exe_result
                return result
        else:
            result = {'status': "1", 'info': "vg name or disk can`t be null"}
            return result

    def vg_remove(self):
        if self.vg_name:
            query_result = self.pvl_info()
            for pvl in query_result:
                if self.vg_name == pvl['vg']:
                    exe_cmd = "vgremove  " + self.vg_name
                    exe_result = exe_command(self.ip, exe_cmd)
                    result = exe_result
                    return result
            result = {'status': "1", 'info': "vg group is not exsit"}
            return result
        else:
            result = {'status': "1", 'info': "vg name  can`t be null"}
            return result

    def vg_extend(self):
        if self.vg_name  and self.new_disk:
            query_result = self.pvl_info()
            for pvl in query_result:
                if self.vg_name == pvl['vg']:
                        exe_cmd = "vgextend  " + self.vg_name+" ".join(self.new_disk)
                        exe_result = exe_command(self.ip, exe_cmd)
                        result = exe_result
                        return result
            result = {'status': "1", 'info': "vg group  is not exsit "}
            return result
        else:
            result = {'status': "1", 'info': "vg name  or disk can`t be null"}
            return result

    def lv_add(self):
        query_result = self.pvl_info()
        if self.lv_name and self.lv_size and self.vg_name:
            for pvl in query_result:
                if self.lv_name == pvl['lv'] :
                    result = {'status': "1", 'info': "lv volume is exsit"}
                    return result
                exe_cmd = "lvcreate  -L " +self.lv_size+" -n "+self.lv_name +" "+self.vg_name
                exe_result = exe_command(self.ip, exe_cmd)
                result = exe_result
                return result
        else:
            result = {'status': "1", 'info': "lv volume lv size or vg name can`t be null"}
            return result

    def lv_remove(self):
        if self.lv_name:
            query_result = self.pvl_info()
            for pvl in query_result:
                if self.lv_name == pvl['lv']:
                    lv_path="/dev/"+pvl['vg']+"/"+self.lv_name
                    exe_cmd = "lvremove  " +lv_path
                    exe_result = exe_command(self.ip, exe_cmd)
                    result = exe_result
                    return result
            result = {'status': "1", 'info': "lv group is not exsit"}
            return result
        else:
            result = {'status': "1", 'info': "lv volume can`t be null"}
            return result

    def lv_extend(self):
        if self.lv_name and self.ex_size:
            query_result = self.pvl_info()
            for pvl in query_result:
                if self.lv_name == pvl['lv']:
                    lv_path = "/dev/" + pvl['vg'] + "/" + self.lv_name
                    exe_cmd = "lvextend  -L +" + self.ex_size +" "+lv_path
                    exe_result = exe_command(self.ip, exe_cmd)
                    result = exe_result
                    return result
            result = {'status': "1", 'info': "lv volume  is not exsit "}
            return result
        else:
            result = {'status': "1", 'info': "lv volume  or extend size can`t be null "}
            return result