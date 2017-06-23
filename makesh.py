import os
dirs = os.listdir("./expression/")
for i in dirs[0:2]:
	print "join " + i + "|",
for j in dirs[2:-1]:
	print "join - " + i + '|',
x = dirs[-1]
print "join - " + x

