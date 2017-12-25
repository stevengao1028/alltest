#!/usr/bin/python
# coding=utf-8
from function import *
from raid import *

def disk_info(ip="127.0.0.1",disk=""):
    #获取系统blk 磁盘信息 ，包含名称，大小，用途的磁盘列表
    exe_cmd = """lsblk |grep disk|awk '{print $1,$4}'"""
    exe_result = exe_command(ip,exe_cmd)
    disk_list = []
    if exe_result['status'] == "0":
        for disk in exe_result['info'].split('\n'):
            disk_info = {'name': "", 'size': "", 'usage': "",'type':""}
            disk_info['name'] = disk.split()[0]
            disk_info['size'] = disk.split()[1]
            disk_list.append(disk_info)
    #到raid中查询
    query_zfs = zfs().zpool_query()
    query_lvm = lvm().pvl_info()
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

