import os

"""
生信编程第4题
shell中join命令可用于关联，但只能关联两个文件，多文件关联可以用管道 | 加选项 -
例如：合并abcde五个txt表达谱文件， join a.txt b.txt | join - c.txt | join - d.txt | join - e.txt
此文本用于生成该命令的sh文件，将expression文件夹下所有文件合并
"""

dirs = os.listdir("./expression/")
for i in dirs[0:2]:		#前两个文件不需要-选项
	print "join " + i + "|",
for j in dirs[2:-1]:
	print "join - " + i + '|',
x = dirs[-1]
print "join - " + x		#避免最后加管道符号|

