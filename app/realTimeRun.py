import pymongo
import subprocess
import time
cmd_1 = 'python3 stock.py TWSE 24_1 '
cmd_2 = 'python3 stock.py TWSE 24_2 '
p = {}
p["0"] = subprocess.Popen(cmd_1,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
p["1"] = subprocess.Popen(cmd_2,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
print(p["0"])
stop = 2
p["0"].wait()
while stop > 0:
    print("code(",p["0"].pid,")=",p["0"].returncode)
    print("code(",p["1"].pid,")=",p["1"].returncode)
    time.sleep(10)
    p["0"].poll()
    p["1"].poll()
    if p["0"].returncode == 0:
        stop = stop - 1
    if p["1"].returncode == 0:
        stop = stop - 1
    print(stop)
