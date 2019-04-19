#!/usr/bin/python
import pymongo
import subprocess
import time
cmd_1 = 'python3 stock.py TWSE "24_1"'
cmd_2 = 'python3 stock.py TWSE "24_2"'
#cmd_3 = 'python3 stock.py TWSE "24_5"'
p = {}
p["0"] = subprocess.Popen(cmd_1, shell=True)
p["1"] = subprocess.Popen(cmd_2, shell=True)
#p["2"] = subprocess.Popen(cmd_3, shell=True)
print(p["0"])
stop = 22 
#p["0"].wait()
while stop > 0:
    print("code(",p["0"].pid,")=",p["0"].returncode)
    print("code(",p["1"].pid,")=",p["1"].returncode)
#    print("code(",p["2"].pid,")=",p["2"].returncode)
    time.sleep(10)
    p["0"].poll()
    p["1"].poll()
#    p["2"].poll()
    if p["0"].returncode == 0:
        stop = stop - 1
        p["0"].kill
    elif p["0"].returncode == None:
        p["0"].poll()
    elif p["0"].returncode != 0:
        p["0"].kill
        p["0"] = subprocess.Popen(cmd_1, shell=True) 

    if p["1"].returncode == 0:
        stop = stop - 1
        p["1"].kill
    elif p["1"].returncode == None:
        p["1"].poll()
    elif p["1"].returncode != 0:
        p["1"].kill
        p["1"] = subprocess.Popen(cmd_2, shell=True)
#    if p["2"].returncode == 0:
#        stop = stop - 1
    print(stop)
