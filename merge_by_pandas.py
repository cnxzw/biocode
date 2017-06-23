#-*-coding:utf-8-*-

"""
@author:xzw
@file:merge_by_pandas.py
@time:2017/6/16 11:06
"""
import pandas
import os
name_list=os.listdir("expression")
fram_list=[pandas.read_table("expression/%s" % name) for name in name_list]
fram=fram_list[0]
for i in range(1,len(fram_list)):
    fram=pandas.merge(fram,fram_list[i])
fram.to_csv("result.csv",index=False)