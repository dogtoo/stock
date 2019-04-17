import pymongo
import os
cmd = 'ps -ef '
textlist = os.popen(cmd).readlines()
print(os.getpid())
for line in textlist:
    print(line)