#-*-coding:utf-8-*-

"""
@author:xzw
@file:test.py
@time:2017/6/14 18:59
"""

import time
import sys
import re
from collections import OrderedDict

start = time.clock()
args = sys.argv

sum_atgc = OrderedDict()
bases = ['A','T','G','C','N']




with open(args[1],'r') as f:
    while 1:
        line = f.readline() #readline 函数可以节省内存
        if not line:
            break
        if line.startswith('>'):
            line = line.rstrip()
            chr_id = re.split(r'>|\s',line)[1][:]
            sum_atgc[chr_id] = OrderedDict()
            for base in bases:
                sum_atgc[chr_id][base] = 0
        else:
            line = line.strip('\n').upper()
            for base in bases:
                sum_atgc[chr_id][base] += line.count(base)



print "chr_id\tA\tG\tT\tC\tN\tGC\tN\tSUM"
for chr_id, atgc_count in sum_atgc.items():
        GC = atgc_count['G'] + atgc_count['C']
        SUM = sum(atgc_count.values())
        print "%s\t" % chr_id,
        for base in bases:
            print "%d\t" % (atgc_count[base]),
        print "%.2f\t" % (GC*1.0/SUM),
        print "%.2f" % (atgc_count['N']*1.0/SUM),
        print "%d" % SUM

end = time.clock()
print "Use %.2f s" % (end-start)

