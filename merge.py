#-*-coding:utf-8-*-

"""
@author:xzw
@file:merge.py
@time:2017/6/15 23:16
"""

"""
生信编程第4题
将多个表达谱合并成一个表达矩阵
数据来源：NCBI/GEO
ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE48nnn/GSE48213/suppl/GSE48213_RAW.tar
"""

import glob
from collections import OrderedDict
import sys


path = sys.argv

MyDict = OrderedDict()

def ReadFile(File):
    with open(File,'r') as f:
        for line in f:
            #if line.startswith('EnsEMBL_Gene_ID'):
                #continue
            lst = line.strip().split('\t')      #strip用于去掉行尾换行符
            gene = lst[0]
            num = lst[1]
            if gene not in MyDict:
                MyDict[gene] = [num]
            else:
                MyDict[gene].append(num)

    return MyDict

def main():
    list_dirs = glob.glob("./expression/*.txt") #glob函数用于读取所有文件
    for i in list_dirs:
        my_dis = ReadFile(i)
    with open('merge.csv','w') as fout:
        for gene,list_num in my_dis.items():
            fout.write(gene + "," + ",".join(list_num) + '\n')

if __name__ == '__main__':
    main()