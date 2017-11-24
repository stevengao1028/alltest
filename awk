计算相同$1的和，数组形式，shell数组类似字典，下标可以是数字，也可是其它,便利数组即可输出下标
cat file |awk '{a[$1]=a[$1]+$2}END{for (i in a){print i,a[i]}}'

文件类似如下：
a 1
b 2
c 3
a 3
b 3
c 2

以数组的形式输出每行,或者指定步长的行，或者指定NR
cat file |awk '{a[NR]=$0}END{for (i=1;i<=NR；i+=1){print a[i]}}'


去重复行，以前面出现的为准，后面重复的去除，默认print $0，默认判断$1 ,可以根据需求判断任何位置
cat file |awk '!a[$1]++'  先取反在自增1
cat file |awk '++a[$1]==1'先自增在判断是否等于1

去重复行，以后面出现的为准，后赋值的保留
cat file |awk '{a[$1]=$0}END{for (i in a){print a[i]}}'

计数，先将相同下标的累加，最后遍历输出下标和值
awk '{a[$1]+=1}END{for (i in a) print i, a[i]}' file

累加
seq 100 |awk '{a+=$1}END{print a}'

行列转换
cat file3 |awk '{for (i=1;i<=NF;i++){a[NR,i]=$i}}END{for (i=1;i<=NF;i++){for (j=1;j<=NR;j++){printf a[j,i]" "}{print ""}}}'


合并文件，匹配相同类容
awk -F" " '{a[$1]=a[$1]$0}END{for (i in a ){print a[i]}}' file1 file2
awk 'NR==FNR{a[$1]=$0}NR!=FNR{$1=a[$1];print $0}' file2 file1

awk 重定向
>第一次清空 ，后面追加
awk '{print >"file"}'
>>追加
awk '{print >>"file"}'
