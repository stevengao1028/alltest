#!/usr/bin/python
# coding=utf-8
from function import *
import re

def disk_info(ip="127.0.0.1",disk=""):
    #获取系统blk 磁盘信息 ，包含名称，大小，用途的磁盘列表
    exe_cmd = """lsscsi -ws |awk '$2~/disk/{print $3,$4}'"""
    exe_result = exe_command(ip,exe_cmd)
    disk_list = []
    if exe_result['status'] == "0" and exe_result['info']:
        for disk in exe_result['info'].split('\n'):
            disk_info = {'name': "", 'size': "", 'usage': "",'type':""}
            disk_info['name'] = disk.split()[0].split('/dev/')[1]
            disk_info['size'] = disk.split()[1]
            disk_list.append(disk_info)
    #到raid中查询
    query_zfs = zpool_info(ip)
    query_lvm = lvm_info(ip)
    for num in range(len(disk_list)):
        for pool in query_zfs:
            if disk_list[num]['name'] in pool['disks'] or disk_list[num]['name'] in pool['spares']:
                disk_list[num]['usage'] = pool['name']
                disk_list[num]['type'] = "zfs"
        for pvl in query_lvm:
            if disk_list[num]['name'] in pvl['pv']:
                disk_list[num]['usage'] = pvl['vg']
                disk_list[num]['type'] = "lvm"
    result = disk_list
    return result

#query_zpool
def zpool_info(ip="127.0.0.1",pool_name=""):
    exe_cmd_pool = "zpool status "+pool_name
    exe_result_pool = exe_command(ip,exe_cmd_pool)
    pool_list =[]
    exe_cmd_zfs = "zfs list -o name,logicalused,volsize,type,used"
    exe_result_zfs = exe_command(ip, exe_cmd_zfs)
    if exe_result_pool['status'] != "0" or exe_result_zfs['status'] != "0" :
        result = {'status': "1", 'info': "lookup fails"}
        return result
    for pool in exe_result_pool['info'].split('errors'):
        pool_info = {'name':'','state':'','disks':[],'spares':[],'raid':'0','volumes':[],'used':'','size':''}
        disks=[]
        spares=[]
        volumes=[]
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
        if exe_result_zfs['info']:
            for vol in exe_result_zfs['info'].split('\n'):
                if  "filesystem" in vol.split()[3]:
                    pool_info['used'] = vol.split()[4]
                elif "volume" in vol.split()[3]:
                    if pool_info['name'] == vol.split()[0].split('/')[0]:
                        vol_name = vol.split()[0].split('/')[1]
                        vol_used = vol.split()[1]
                        vol_size = vol.split()[2]
                        vol_info = {'vol_name':vol_name,'vol_used':vol_used,'vol_size':vol_size}
                        volumes.append(vol_info)
            pool_info['volumes'] = volumes
        if pool_info['name']:
            pool_list.append(pool_info)
    result = pool_list
    return result

def lvm_info(ip="127.0.0.1"):
    exe_cmd = """pvs -o pv_name,vg_name,lv_name"""
    exe_result = exe_command(ip,exe_cmd)
    pvl = []
    if exe_result['status'] == "0":
        for list in exe_result['info'].split('\n'):
            if re.match(r'  /dev', list):
                pv_info={'pv':"",'vg':"",'lv':""}
                pv_info['pv'] = list.split()[0].split('/dev/')[1]
                if len(list.split()) == 2:
                    pv_info['vg'] = list.split()[1]
                if len(list.split()) == 3:
                    pv_info['vg'] = list.split()[1]
                    pv_info['lv'] = list.split()[2]
                pvl.append(pv_info)
    result = pvl
    return result