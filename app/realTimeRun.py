import pymongo
import os
cmd = 'ps -ef '
textlist = os.popen(cmd).readlines()
for line in textlist:
    print(line)