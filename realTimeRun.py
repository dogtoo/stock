#!/usr/bin/python
import pymongo
import subprocess
import time
from datetime import timedelta, date, datetime
import os
import logging

import configparser
config = configparser.ConfigParser()
config.read('config.ini')
statics = configparser.ConfigParser()
statics.read('statics.ini')

if config['stock']['logginglevel'] == 'DEBUG':
    level = logging.DEBUG
elif config['stock']['logginglevel'] == 'INFO':
    level = logging.INFO
elif config['stock']['logginglevel'] == 'ERROR':
    level = logging.ERROR


def writeIni():
    with open('statics.ini', 'w') as staticsFile:
        statics.write(staticsFile)


logging.basicConfig(level=level,
                    format='%(asctime)s - %(levelname)s : %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    filename=config['stock']['logfilelink'] + 'realTime_{:%Y-%m-%d}.log'.format(datetime.now()))
# filename='/python/log/realTime_{:%Y-%m-%d}.log'.format(datetime.now()))

stockList = ["01", "02", "03", "04", "05", "06", "08", "09", "10", "11", "12", "14", "15",
             "16", "17", "18", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
#stockList = ["01"]
cmd = 'python ./stock.py TWSE "{}"'
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
# logging.debug("Files in '%s': %s" % (cwd, files))
statics['static']['enabled'] = 'True'
writeIni()


def runCom(L):
    time.sleep(3)
    return subprocess.Popen(cmd.format(L), shell=True)


p = list(map(runCom, stockList))

stockListTPEX = ["02", "03", "04", "05", "06", "10", "11", "14", "15", "16", "17", "18",
                 "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34"]
#stockListTPEX = ["02"]
cmdTPEX = 'python ./stock.py TPEX "{}"'


def runComTPEX(L):
    time.sleep(3)
    return subprocess.Popen(cmdTPEX.format(L), shell=True)


p.extend(list(map(runComTPEX, stockListTPEX)))


# def logW(L):
#     return open("/python/log/stock{}.log".format(L.replace("|", "_"), "a+"))
#fp = list( map(logW, stockList))

def showStatic(L):
    print(statics['TWSE']['TW'+L])


def showTPStatic(L):
    print(statics['TPEX']['TP'+L])


all = len(stockList)+len(stockListTPEX)
stop = 0

while stop < all:
    inrun = 0
    # map(showStatic, stockList)
    # map(showTPStatic, stockListTPEX)
    for i in range(len(stockList)+len(stockListTPEX)):
        idx = i - 1
        # fp[i].write(p[i].stdout.readline())
        p[idx].poll()
        # logging.info(
        #     str(i) + " code(" + str(p[i].pid) + ")=" + str(p[i].returncode))
        if p[idx].returncode == 0:
            p[idx].kill
        elif p[idx].returncode == None:
            # p[i].poll()
            inrun = inrun + 1
            None
        elif p[idx].returncode != 0:
            p[idx].kill
            p[idx] = subprocess.Popen(cmd.format(stockList[idx]), shell=True)

    stop = all - inrun
    logging.info("have %s in run, %s in stop", inrun, stop)
    time.sleep(5)


# for i in range(len(stockList)):
#     p[i].close()
