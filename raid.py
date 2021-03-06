#!/usr/bin/python
# coding=utf-8
from function import *
from system_info import *

class zfs():
    def __init__(self,ip="127.0.0.1",pool_name="",raid="0",disks=[],spares=[],old_disk="",new_disk="",zfs_name="",zfs_size=""):
        self.ip=ip
        self.pool_name=pool_name
        self.raid=raid
        self.disks=disks
        self.spares=spares
        self.old_disk=old_disk
        self.new_disk=new_disk
        self.zfs_name = zfs_name
        self.zfs_size = zfs_size

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


    #add_zpool
    def zpool_add(self):
        if self.pool_name == "":
            result={'status':"1",'info':"pool name can`t be null"}
            return result
        if self.raid == "5":
            raid_level="raidz1"
        elif self.raid == "6":
            raid_level="raidz2"
        elif self.raid == "0":
            raid_level=""
        else :
            result={'status':"1",'info':"raid level did not been define"}
            return result
        query_result=zpool_info(self.ip,self.pool_name)
        if query_result :
            result={'status':"1",'info':"pool is exsit"}
            return result
        elif self.disks :
            if self.spares:
                exe_cmd="zpool create "+self.pool_name+' '+raid_level+' '+' '.join(self.disks)+' spare '+' '.join(self.spares)+' -f'
            else:
                exe_cmd = "zpool create " +self.pool_name + ' ' + raid_level + ' ' + ' '.join(self.disks)+' -f'
            exe_result=exe_command(self.ip,exe_cmd)
            result=exe_result
            return result
        else:
            result={'status':"1",'info':"disk can`t be null"}
            return result

    #del_zpool
    def zpool_del(self):
        if self.pool_name == "":
            result={'status':"1",'info':"pool name can`t be null"}
            return result
        query_result=zpool_info(self.ip,self.pool_name)
        if query_result :
            exe_cmd="zpool destroy "+self.pool_name
            exe_result = exe_command(self.ip,exe_cmd)
            result = exe_result
            return result
        else:
            result={'status':"1",'info':"pool isn`t exsit"}
            return result

    #replace
    def replace_disk(self):
        if self.pool_name == "" or self.old_disk == "" or self.new_disk == "":
            result={'status':"1",'info':"pool name ,old disk or new disk can`t be null"}
            return result
        query_result=zpool_info(self.ip,self.pool_name)
        if query_result :
            exe_cmd="zpool replace "+self.pool_name+' '+self.old_disk+' '+self.new_disk
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
            return result
        else:
            result={'status':"1",'info':"pool isn`t exsit"}
            return result


    def zfs_add(self):
        if self.pool_name == "" or self.zfs_name == "" or self.zfs_size == "":
            result={'status':"1",'info':"pool name ,zfs name or zfs size can`t be null"}
            return result
        query_result = zpool_info(self.ip,self.pool_name)
        if query_result:
            for volume in query_result[0]['volumes']:
                if volume['vol_name'] == self.zfs_name:
                    result = {'status': "1", 'info': "vol is exsit "}
                    return result
            exe_cmd = "zfs create -V " + self.zfs_size + ' ' + self.pool_name + '/' + self.zfs_name
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
            return result
        else:
            result={'status':"1",'info':"pool isn`t exsit"}
            return result

    def zfs_del(self):
        if self.pool_name == "" or self.zfs_name == "" :
            result={'status':"1",'info':"pool name or zfs name can`t be null"}
            return result
        query_result=zpool_info(self.ip,self.pool_name)
        if query_result:
            for volume in query_result[0]['volumes']:
                if volume['vol_name'] == self.zfs_name:
                    exe_cmd = "zfs destroy " + self.pool_name + '/' + self.zfs_name
                    exe_result = exe_command(self.ip, exe_cmd)
                    result = exe_result
                    return result
            result = {'status': "1", 'info': "vol  isn`t exsit "}
            return result
        else:
            result={'status':"1",'info':"pool isn`t exsit"}
            return result



class lvm():
    def __init__(self,ip="127.0.0.1",vg_name="",lv_name="",lv_size="",ex_size="",new_disk=[],vg_disk=[],pv_disk=[]):
        self.ip = ip
        self.vg_name = vg_name
        self.lv_name = lv_name
        self.lv_size = lv_size
        self.ex_size = ex_size
        self.new_disk = new_disk
        self.vg_disk = vg_disk
        self.pv_disk = pv_disk

    # def pv_query(self):
    #     exe_cmd="""pvs -o pv_name,pv_size,lv_name,lv_size,vg_size,vg_free,vg_name"""

    def pv_add(self):
        if self.pv_disk:
            exe_cmd = "pvcreate  "+" ".join(self.pv_disk)
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
        else:
                result = {'status': "1", 'info': "disk can`t be null"}
        return result

    def pv_remove(self):
        if  self.pv_disk:
            exe_cmd = "pvremove  " +" ".join(self.pv_disk)
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
        else:
            result = {'status': "1", 'info': "disk can`t be null"}
        return result

    def vg_add(self):
        query_result = lvm_info(self.ip,self.vg_name)
        if self.vg_name and self.vg_disk and not query_result:
            exe_cmd = "vgcreate  " + self.vg_name +" "+" ".join(self.vg_disk)+" -y"
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
            return result
        else:
            result = {'status': "1", 'info': "vg name or disk can`t be null | vg group is exsit"}
            return result

    def vg_remove(self):
        query_result = lvm_info(self.ip, self.vg_name)
        if self.vg_name and query_result:
                exe_cmd = "vgremove  " + self.vg_name+" -y"
                exe_result = exe_command(self.ip, exe_cmd)
                result = exe_result
                return result
        else:
            result = {'status': "1", 'info': "vg name can`t be null |vg is not exsit"}
            return result

    def vg_extend(self):
        query_result = lvm_info(self.ip, self.vg_name)
        if self.vg_name  and self.new_disk and query_result:
            exe_cmd = "vgextend  " + self.vg_name+" "+" ".join(self.new_disk)+" -y"
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
            return result
        else:
            result = {'status': "1", 'info': "vg name or disk can`t be null | vg group is not exsit"}
            return result

    def lv_add(self):
        query_result = lvm_info(self.ip, self.vg_name)
        if self.lv_name and self.lv_size and self.vg_name and query_result:
            if self.lv_name in query_result[0]['lv']:
                result = {'status': "1", 'info': "lv volume is exsit"}
                return result
            exe_cmd = "lvcreate  -L " +self.lv_size+" -n "+self.lv_name +" "+self.vg_name+" -y"
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
            return result
        else:
            result = {'status': "1", 'info': "lv volume|size or vg name can`t be null | vg group is not exsit "}
            return result

    def lv_remove(self):
        query_result = lvm_info(self.ip, self.vg_name)
        if self.lv_name and self.vg_name and query_result:
            if  self.lv_name in query_result[0]['lv']:
                lv_path="/dev/"+self.vg_name+"/"+self.lv_name
                exe_cmd = "lvremove  " +lv_path+" -y"
                exe_result = exe_command(self.ip, exe_cmd)
                result = exe_result
                return result
            result = {'status': "1", 'info': "lv volume is not exsit"}
            return result
        else:
            result = {'status': "1", 'info': "vg group or lv volume can`t be null | vg group is not exsit "}
            return result

    def lv_extend(self):
        query_result = lvm_info(self.ip, self.vg_name)
        if self.lv_name and self.ex_size and query_result:
            if self.lv_name in query_result[0]['lv']:
                lv_path = "/dev/" + self.vg_name + "/" + self.lv_name
                exe_cmd = "lvextend  -L +" + self.ex_size +" "+lv_path+" -y"
                exe_result = exe_command(self.ip, exe_cmd)
                result = exe_result
                return result
            result = {'status': "1", 'info': "lv volume  is not exsit "}
            return result
        else:
            result = {'status': "1", 'info': "lv volume or extend size can`t be null | vg group is not exsit"}
            return result

class md():
    def __init__(self, ip="127.0.0.1",raid="",md_name="",disk=[],spare=[],new_disk=[]):
        self.ip = ip
        self.md_name = md_name
        self.raid = raid
        self.spare = spare
        self.disk = disk
        self.new_disk = new_disk

    def md_add(self):
        query_result = md_info(self.ip, self.md_name)
        if self.md_name and self.disk and not query_result:
            disk_num = str(len(self.disk))
            spare_num = str(len(self.spare))
            if self.spare:
                exe_cmd = "mdadm --create /dev/" + self.md_name + " --level=" + self.raid + " --raid-devices=" + disk_num +" "+" ".join(self.disk) + " spare-devices=" + spare_num +" "+ " ".join(self.spare)
            else:
                exe_cmd = "mdadm --create /dev/" + self.md_name + " --level=" + self.raid + " --raid-devices=" + disk_num +" "+ " ".join(self.disk)
            exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
            return result
        else:
            result = {'status': "1", 'info': "md name or disk can`t be null | md group is exsit"}
            return result

    def md_del(self):
        query_result = md_info(self.ip, self.md_name)
        if self.md_name and  query_result:
            exe_cmd = "mdadm -S /dev/" + self.md_name
            exe_result = exe_command(self.ip, exe_cmd)
            if exe_result['status'] == "0":
                exe_cmd = "mdadm --zero-superblock " + self.md_name+" ".join(self.disk)
                exe_result = exe_command(self.ip, exe_cmd)
            result = exe_result
            return result
        else:
            result = {'status': "1", 'info': "md name cant be null |md name isn`t exsit"}
            return result

