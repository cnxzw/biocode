#-*-coding:utf-8-*-

"""
@author:xzw
@file:kegg.py
@time:2017/6/25 14:48
"""

"""
生信编程第6题
下载最新版KEGG并且解析好
数据来源：KEGG keg格式
http://www.genome.jp/kegg-bin/download_htext?htext=ko00001.keg&format=htext&filedir=
"""

import sys
import re
from collections import OrderedDict

args = sys.argv
hsa_kegg = OrderedDict()

with open(args[1],'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('A'):
            mch = re.search('A<b>(.+)</b>',line)
            className = mch.group(1)
            hsa_kegg[className] = OrderedDict()

        elif line.startswith('B'):
            if line == 'B':
                continue
            else:
                mch = re.search('<b>(.+)</b>',line)
                subClass = mch.group(1)
                hsa_kegg[className][subClass] = OrderedDict()

        elif line.startswith('C'):
            mch = re.search('(\d+)\s(.+)',line)
            pathID = 'hsa' + mch.group(1)
            pathName = re.sub('\s\[.+\]','',mch.group(2))
            pathway = pathID + ':' + pathName
            hsa_kegg[className][subClass][pathway] = [[],[]]

        elif line.startswith('D'):
            lst = line.split(';')
            geneInfo = lst[0].split('\t')
            mch = re.match('D\s+(\d+)\s(.+)',geneInfo[0])
            geneID = mch.group(1)
            gene = mch.group(2)

            hsa_kegg[className][subClass][pathway][0].append(gene)
            hsa_kegg[className][subClass][pathway][1].append(geneID)

fh = open(args[2],'wt')
for ke,val in hsa_kegg.items():
    for subk,subv in val.items():
        for ptwy, geneList in subv.items():
            genes = ';'.join(geneList[0])
            geneIDs = ';'.join(geneList[1])
            fh.write('\t'.join([ke,subk,ptwy,genes,geneIDs]) + '\n')

fh.close()

pathNum = 0
allgene = []

with open(args[2],'r') as fr:
    for line in fr:
        lst = line.strip().split('\t')
        if len(lst) > 3:
            pathNum += 1
            geneList = lst[-2].split(';')
            allgene.extend(geneList)

    print "The number of pathways is %d" % (pathNum)
    print "The num of gene is %d" % len(set(allgene))


