# coding=utf-8
import commands
import json

#exe_command 
def exe_command(exe_cmd):
	(status,output)=commands.getstatusoutput(exe_cmd)
	result={'status':status,'info':output}
	result=json.dumps(result)
	return result


#pre-check system mod
def check_mod():
	(status,output)=commands.getstatusoutput('zpool status')
	if status != 0:
			exe_cmd="modprobe zfs"
			result=exe_command(exe_cmd)
			return result
	data={'status':status,'info':output}
	result=json.dumps(data)
	return result

#query_zpool
def zpool_query(pool_name=""):
	exe_cmd="""zpool status """+pool_name+"""  2>/dev/null|awk -F" " '$1~/^pool:/{name=$2}$1~/^sd/{rdisk["\\"",$1,"\\""]=$2}$1~/errors:/{printf "{\\"name\\":\\""name"\\",";for (i in rdisk){printf i":\\""rdisk[i]"\\","}{printf "},"}}END{print ""}'|sed 's/,}/}/g;s/,$//;s/^/[/;s/$/]/'"""
	result=exe_command(exe_cmd)
	return result

#add_zpool
def zpool_add(pool_name,raid,disks,spares=""):
	if raid == 5:
		raid_level="raidz1"
	if raid == 6:
		raid_level="raidz2"
	if raid == 0:
		raid_level=""
	if raid == "":
		result={'status':1,'info':"raid level did not been define"}
		result=json.dumps(result)
		return result
	if pool_name == "":
		result={'status':1,'info':"pool name can`t be null"}
		result=json.dumps(result)
		return result
	query_result=zpool_query(pool_name)
	if query_result['status'] == 0:
		result={'status':1,'info':"pool is exsit"}
		result=json.dumps(result)
		return result
	if disks :
		exe_cmd="zpool create "+pool_name+' '+raid_level+' '+' '.join(disks)+' '+' '.join(spares)
		result=exe_command(exe_cmd)
		result=json.dumps(result)
	else:
		result={'status':1,'info':"disk can`t be null"}
		result=json.dumps(result)
		return result

#del_zpool
def zpool_del(pool_name):
	if pool_name == "":
		result={'status':1,'info':"pool name can`t be null"}
		result=json.dumps(result)
		return result
	query_result=zpool_query(pool_name)
	if query_result['status'] == 0:
		exe_cmd="zpool destroy "+pool_name
		result=exe_command(exe_cmd)
		return result
	else:
		result={'status':1,'info':"pool isn`t exsit"}
		result=json.dumps(result)
		return result


#replace
def replace_disk(pool_name,old_disk,new_disk):
	if pool_name == "" or old_disk == "" or new_disk == "":
		result={'status':1,'info':"pool name ,old disk or new disk can`t be null"}
		result=json.dumps(result)
		return result
	query_result=zpool_query(pool_name)
	if query_result['status'] == 0:
		exe_cmd="zpool replace "+pool_name+' '+old_disk+' '+new_disk
		result=exe_command(exe_cmd)
		return result
	else:
		result={'status':1,'info':"pool isn`t exsit"}
		result=json.dumps(result)
		return result

