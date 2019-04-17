import pymongo
import so
cmd = 'ps -ef '
textlist = os.popen(cmd).readlines()
for line in textlist:
    print(line)