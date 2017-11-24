先匹配字符的行，在执行替换
sed -e '/IPADDR/s/[0-9].*/192.168.0.22/g' ifcfg-ens32

加外部变量'$a'
sed -e '/IPADDR/s/IPADDR.*/IPADDR='$a'/g;/NETMASK/s/[0-9].*/255.222.222.222/g' ifcfg-ens32 

将比较复杂的部分写在文件内
sed -f filename 



直接替换行
sed -e '/IPADDR/cIPADDR='$a'' ifcfg-ens32 
