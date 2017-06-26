#-*-coding:utf-8-*-

"""
@author:xzw
@file:calculate_exons.py
@time:2017/6/14 10:52
"""

"""
生信编程第1题
计算CCDS_current.txt中外显子累计长度
数据来源：NCBI
ftp://ftp.ncbi.nlm.nih.gov/pub/CCDS/current_human/CCDS.current.txt
"""

import sys
import re

args = sys.argv
SUM = 0
dct = {}

with open(args[1],'r') as f:
    for line in f:
        if line.startswith('#'):
            continue

        line = line.rstrip()
        lst = line.split('\t')
        if lst[-2] == '-':
            continue

        #exons = lst[-2].lstrip('[').rstrip(']').split(', ')
        lst[-2] = re.sub('\[|\]','',lst[-2])  #去掉中括号
        exons = lst[-2].split(', ')
        chr = lst[0]

        for exon in exons:
            start = int(exon.split('-')[0])
            end = int(exon.split('-')[1])
            length = end - start
            coordinate = chr + ':' + exon
            if coordinate not in dct:
                dct[coordinate] = 1
                SUM += length

print SUM