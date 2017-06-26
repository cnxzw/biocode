#-*-coding:utf-8-*-

"""
@author:xzw
@file:hg19.py
@time:2017/6/14 18:31
"""

"""
生信编程第2题
统计hg19基因组每条染色体长度、N、GC含量
数据来源：UCSC
ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz
"""

import re
import sys
import time
from collections import OrderedDict     #有序字典

start = time.clock()
args = sys.argv
sum_atgc = OrderedDict()
bases = ['A','T','G','C','N']


def get_chr(buffer):
    (buffer,tmp) = buffer.split('>',1)
    if '>' not in tmp:
        return (buffer, tmp)
    else:
        get_chr(tmp)
        reutrn(buffer, get_chr(tmp))


def get_list(tmp):
    tmp_list = []
    while len(tmp) > 1 and type(tmp) == tuple:
        tmp_list.append(tmp[0])
        tmp = tmp[1]
    tmp_list.append(tmp)
    return tmp_list


with open(args[1],'r') as Fin:
    tmp = Fin.readline()    #读取第一行
    chr_id = re.split(r'\s', tmp)[0][1:]
    sum_atgc[chr_id] = OrderedDict()

    for base in bases:
        sum_atgc[chr_id][base] = 0  #初始化第一行各碱基数目

    while 1:
        buffer = Fin.read(1024*1024)
        if not buffer:
            break       #while句型常用于不规律文本，要有终止条件

        if '>' in buffer:
            (buffer,tmps) = get_chr(buffer)
            if len(tmps) > 1:
                tmp = get_list(tmps)
            buffer = buffer.upper()
            for base in bases:
                sum_atgc[chr_id][base] += buffer.count(base)

            for tmp in tmps:
                (tmp, buffer) = tmp.split('\n', 1)
                chr_id = re.split(r'\s', tmp)[0][:]
                sum_atgc[chr_id] = OrderedDict()

            for base in bases:
                sum_atgc[chr_id][base] = 0

            buffer = buffer.upper()
            for base in bases:
                sum_atgc[chr_id][base] += buffer.count(base)

        else:
            buffer = buffer.upper()
            for base in bases:
                sum_atgc[chr_id][base] += buffer.count(base)

for chr_id, atgc_count in sum_atgc.items():
    GC = atgc_count['G'] + atgc_count['C']
    SUM = sum(atgc_count.values())
    print chr_id
    for base in bases:
        print "%s : %s" % (base, atgc_count[base])
    print "GC : %.2f" % (GC*1.0/SUM)
    print "N : %.2f" % (atgc_count['N']*1.0/SUM)
    print "SUM : %s" % (SUM)
    print "\n"

end = time.clock()
print "Use %s s" % (str(end-start))