# -*- coding: utf-8 -*-
import urllib2
import re
import datetime
import sqlite3
# import numpy as ap
sum=0
end_num=34
data = range(6)
i=0
# time={}
# for i in range(21,186):
#     time[str(i)]=0
# # print time
for one in range(1,28):
    data[0]=one
    for two in range(one+1,29):
        data[1] = two
        for three in range(two+1, 30):
            data[2] = three
            for four in range(three + 1, 31):
                data[3] = four
                for five in range(four + 1, 32):
                    data[4] = five
                    for six in range(five + 1, 33):
                        data[5] = six
                        # print data
                        i+=1

print i
                        # print sum(data)
                        # s = 0
                        # for x in data:
                        #     s += x
                        #
                        # each_time=time[str(s)]+1
                        # time[str(s)]=each_time
                        # each_time=0
                        # print s,time[str(s)]
                        # for blue in range(16):
#                         #     i=i+1
# for i in time:
#     print i,time[i]# print len(data)
                            # data_sum=sum(data)
                            # if data_sum==8 and data not in data_list:
                            #     data_list = append(data.sort())
                            #     print one,two,three,four,five,six,sum








