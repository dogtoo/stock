#!/usr/bin/python
import pymongo
import subprocess
import time

stockList = ["01|02","20","03","21","12","04|18|14","28","05|22","06|08|09","10|11|15","25|24","31|27","26|29","39|23|16|17","00"]

cmd = 'python3 stock.py TWSE "{}"'

def runCom(L):
    return subprocess.Popen(cmd.format(L), shell=True)

p = list( map(runCom, stockList)) 

stop = len(stockList)

while stop > 0:
    for i in range(len(stockList)):
        print(i," code(",p[i].pid,")=",p[i].returncode)
        p[i].poll()
        if p[i].returncode == 0:
            stop = stop - 1
            p[i].kill
        elif p[i].returncode == None:
            p[i].poll()
        elif p[i].returncode != 0:
            p[i].kill
            p[i] = subprocess.Popen(cmd_1, shell=True)
            
    time.sleep(10)
    print(stop)
