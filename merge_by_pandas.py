#-*-coding:utf-8-*-

"""
@author:xzw
@file:merge_by_pandas.py
@time:2017/6/16 11:06
"""

"""
生信编程第4题
使用pandas将多个表达谱合并成一个表达矩阵
数据来源：NCBI/GEO
ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE48nnn/GSE48213/suppl/GSE48213_RAW.tar
"""

import pandas
import os
name_list=os.listdir("expression")
fram_list=[pandas.read_table("expression/%s" % name) for name in name_list]
fram=fram_list[0]
for i in range(1,len(fram_list)):
    fram=pandas.merge(fram,fram_list[i])
fram.to_csv("result.csv",index=False)