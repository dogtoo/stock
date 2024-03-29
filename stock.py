#!/usr/bin/python
# print("twStockTest")
import configparser
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
from requests.adapters import HTTPAdapter
from datetime import timedelta, date, datetime
import twstock
import pymongo
import time
import sys
import logging
import requests
import random
random.seed('dogtoo')

debug = False
stockName = sys.argv[1]
runGroupStr = ""
runGroupStr = sys.argv[2]
if len(runGroupStr) == 0:
    runGroupStr = "24"

sname = "TW"
if stockName == 'TPEX':
    sname = "TP"

sname = sname + runGroupStr

config = configparser.ConfigParser()
config.read('config.ini')
statics = configparser.ConfigParser()
statics.read('statics.ini')

if config['stock']['logginglevel'] == 'DEBUG':
    level = logging.DEBUG
    debug = True
elif config['stock']['logginglevel'] == 'INFO':
    level = logging.INFO
elif config['stock']['logginglevel'] == 'ERROR':
    level = logging.ERROR

SESSION_URL = 'https://mis.twse.com.tw'
logging.basicConfig(level=level,
                    format='%(asctime)s - %(levelname)s : %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    filename=config['stock']['logfilelink'] + '{:%Y-%m-%d}'.format(datetime.now()) + '/' + stockName + '_' + '{}.log'.format(runGroupStr.replace("|", "_")))
# filename='/python/log/' + stockName + '_' + '{:%Y-%m-%d}'.format(datetime.now()) + '_' + '{}.log'.format(runGroupStr.replace("|","_")) )


client = pymongo.MongoClient(
    host=config['stock']['dbConn'],
    port=int(config['stock']['port']),
    username=config['stock']['dbuser'],
    password=config['stock']['dbpass'],
    authSource="twStock")
#client = pymongo.MongoClient("mongodb://192.168.1.5:27017")
db = client["twStock"]
# db.authenticate("twstock", "twstock123")

collname = ""
if debug:
    collname = "realtime_bak"
else:
    collname = "realtime"
collRT = db[collname]
collSt = db[stockName]
#runGroupSet = set(runGroupStr.split(","))

# 每日下午13:31分為止
"""
localtime = time.localtime() # get struct_time
today = time.strftime("%Y%m%d", localtime)

localtime = int(time.mktime(localtime)) #系統時間
strtime = int(time.mktime(time.strptime(today + ' 00:50:00', '%Y%m%d %H:%M:%S'))) # 8:50 起
endtime = int(time.mktime(time.strptime(today + ' 05:32:00', '%Y%m%d %H:%M:%S'))) # 13:30 結束
twoEndtime = int(time.mktime(time.strptime(today + ' 06:50:00', '%Y%m%d %H:%M:%S'))) # 14:30 
"""
#print("localtime:", localtime, ", Str time:", strtime, ", End time:", endtime, flush=True)

# proxList = ['59.149.159.230:8888'
# , '23.101.2.247:81'
# , '188.166.119.186:80'
# , '178.62.232.215:8080'
# , '192.81.223.236:3128'
# , '62.33.207.197:3128'
# , '62.33.207.202:80'
# , '58.233.211.104:443'
# , '58.233.211.104:80'
# , '109.86.229.189:8080'
# , '51.158.178.67:3128'
# , '51.158.68.26:8811'
# , '51.158.106.54:8811'
# , '58.233.211.104:80'
# , '58.233.211.104:443'
# , '23.237.173.102:3128'
# , '167.172.140.184:3128'
# , '167.172.225.187:3128'
# , '167.172.225.187:8080'
# , '51.158.68.133:8811'
# , '51.158.98.121:8811'
# , '163.172.147.94:8811'
# , '136.243.47.220:3128'
# , '23.101.2.247:81'
# , '159.138.1.185:80'
# , '194.167.44.91:80'
# , '51.158.120.84:8811'
# , '51.158.98.121:8811'
# , '163.172.152.52:8811'
# , '163.172.136.226:8811'
# , '51.158.111.229:8811'
# , '51.158.68.68:8811'
# , '163.172.147.94:8811'
# , '51.158.99.51:8811'
# , '51.158.119.88:8811'
# , '34.90.113.143:3128'
# , '141.125.82.106:80'
# , '138.201.72.117:80'
# , '185.125.204.68:3128'
# , '103.226.213.156:8888'
# , '176.123.61.238:3128'
# , '62.33.207.201:3128'
# , '150.109.162.73:3128'
# , '67.63.33.7:80'
# , '167.71.132.188:8080'
# , '157.245.207.190:8080'
# , '178.62.232.215:8080'
# , '192.81.223.236:3128'
# , '80.234.38.44:3128'
# , '109.174.19.134:8385'
# , '51.68.189.52:3128'
# , '47.74.44.84:8080'
# , '47.52.32.109:80'
# , '35.235.75.244:3128'
# , '47.52.225.33:80'
# , '157.245.196.253:8080'
# , '159.65.87.167:8080'
# , '149.28.141.62:8118'
# , '167.88.117.209:8080'
# , '47.52.131.183:80'
# , '206.189.200.179:8080'
# , '159.65.109.226:8080'
# , '167.71.138.113:8080'
# , '165.22.241.186:8080'
# , '209.97.128.45:8080'
# , '165.22.254.99:3128'
# ]

proxList = ['23.91.219.238:8080', '182.253.115.90:8080', '61.19.40.50:57474', '117.121.213.53:3128', '51.75.83.94:8080', '140.227.167.60:3128', '36.67.89.179:65205', '182.253.115.66:57733', '103.96.118.27:8080', '119.2.54.204:44860', '124.219.176.139:39589', '182.52.51.59:38238', '125.26.99.186:52680', '1.10.186.114:55824', '24.172.82.94:53281', '1.10.188.140:43327', '61.5.80.165:8080', '117.121.213.171:3128', '36.89.106.247:43184', '34.83.71.102:8080', '195.4.168.40:8080', '183.88.192.241:8080', '116.254.100.165:46675', '125.25.80.39:42790', '209.97.164.211:47503', '197.245.230.122:48918', '173.46.67.172:58517', '45.64.99.28:8080', '125.25.165.106:43730', '144.91.116.171:443', '36.89.181.155:60165', '182.52.51.154:32563', '1.10.189.68:60400', '139.194.123.245:8080', '125.162.141.70:33100', '202.150.139.46:59979', '103.83.178.174:4145', '70.60.132.34:1080', '97.90.49.141:54321', '47.99.65.77:3128', '114.4.192.17:4145', '114.104.189.119:1080', '64.227.2.136:8080', '58.58.213.55:8888', '74.214.177.61:8080', '103.83.179.153:4145', '70.169.129.246:48678', '58.49.116.78:30957', '103.23.102.245:4145', '103.69.118.77:4145', '36.89.229.97:35098', '52.80.58.248:3128', '68.183.237.129:8080', '61.164.34.4:80', '54.213.173.231:80', '112.6.132.95:51080', '36.89.169.170:8080', '36.90.123.171:8181', '60.216.101.46:49327', '113.229.81.108:1080', '70.169.70.90:80', '36.89.189.137:46537', '36.89.93.28:8080', '54.174.159.255:8080', '39.137.69.6:80', '103.36.35.135:8080', '183.146.213.157:80', '51.91.212.159:3128', '206.201.6.117:8080', '104.236.48.178:8080', '144.91.116.171:80', '121.40.141.226:31280', '103.20.189.126:3128', '219.85.16.213:255', '50.203.239.20:80', '163.172.152.52:8811', '163.172.189.32:8811', '122.224.65.201:3128', '70.165.64.33:48678', '18.210.69.172:3128', '113.53.230.167:80', '51.158.108.135:8811', '45.112.127.23:8080', '103.228.117.244:8080', '163.172.190.160:8811', '110.78.20.62:3128', '51.158.99.51:8811', '163.172.136.226:8811', '34.90.113.143:3128', '70.169.149.231:48678', '107.190.148.202:50854', '70.169.132.131:48678', '36.67.66.202:55638', '191.96.42.80:3128', '103.86.156.150:43122'
            ]

group = {}
stockCodeL = []
qurySt = collSt.find({'groupCode': {'$regex': runGroupStr}}, {
                     "_id": 0, "code": 1, "groupCode": 1})
for st in qurySt:
    if st['groupCode'] == '00':
        continue
    stockCodeL.append(st['code'])  # 這次要查的股票們
    group[st['code']] = st['groupCode']  # 用股票號碼回頭找group
    """
    #查詢股票群組
    for stockCName,codeL in st.items():
        stockCodeL = []
        if stockCName == "OTHER":
            continue
        #同組股票代碼
        stockGroupCode = "00"
        for code,t in codeL.items():
            if 'groupCode' in t:
                stockGroupCode = t["groupCode"]
            stockCodeL.append(code)
        #只跑指定的組
        if stockGroupCode not in runGroupSet:
            continue
        group[stockGroupCode]=stockCodeL
        print(stockCName + "(" + stockGroupCode + ")" + " " + str(len(stockCodeL)), flush=True)
    """


"""
localtime = time.localtime() # get struct_time
today = time.strftime("%Y%m%d", localtime)

localtime = int(time.mktime(localtime)) #系統時間
strtime = int(time.mktime(time.strptime(today + ' 00:50:00', '%Y%m%d %H:%M:%S'))) # 8:50 起
endtime = int(time.mktime(time.strptime(today + ' 05:32:00', '%Y%m%d %H:%M:%S'))) # 13:30 結束
twoEndtime = int(time.mktime(time.strptime(today + ' 06:50:00', '%Y%m%d %H:%M:%S'))) # 14:30 
"""


def chkRun(runcnt):
    sysTime = int('{:%d%H%M}'.format(datetime.now()))
    # 9:00 起
    strTime = int('{:%d}'.format(datetime.now()) + '0859')
    # 13:40 結束
    endTime = int('{:%d}'.format(datetime.now()) + '1340')
    # 15:00 零股結算
    secBTime = int('{:%d}'.format(datetime.now()) + '1459')
    secETime = int('{:%d}'.format(datetime.now()) + '1510')
    logging.debug("sysTime = " + str(sysTime) + ", strTime = " + str(strTime) + ", endTime = " +
                  str(endTime) + ", secBTime = " + str(secBTime) + ", secETime = " + str(secETime))
    if debug:
        logging.debug("is debug mode")
        return True
    elif sysTime > strTime and sysTime < endTime:
        return True
    elif sysTime > secBTime and sysTime < secETime:
        return True
    else:
        logging.info("STOP")
        return False


#print("***" + time.ctime() + "*** (", len(stockCodeL), ")", flush=True)
#logging.error("***" + '{:%H:%M:%S}'.format(datetime.now()) + "*** " + runGroupStr + " (" + str(len(stockCodeL)) + ")")
logging.info(" gropuCode = " + runGroupStr +
             "(cnt = " + str(len(stockCodeL)) + ")")
run = True
run = chkRun(0)
# while (localtime >= strtime and localtime <= endtime) or debug == True or (localtime > endtime and localtime <= twoEndtime):

proxidx = 0
proxies = {}


class SSLContextAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        kwargs['ssl_context'] = context
        context.load_default_certs()  # this loads the OS defaults on Windows
        return super(SSLContextAdapter, self).init_poolmanager(*args, **kwargs)


req = requests.Session()


def lookStop():
    statics.read('statics.ini')
    if statics['static']['enabled'] == 'True':
        return False
    else:
        logging.info("STOP")
        statics.set(stockName, sname, "STOP")
        sys.exit(0)


def getNewSession():
    getSession = True
    while getSession:
        if not chkRun(0):
            sys.exit(0)
        try:
            if runGroupStr != '01':
                proxies = {"http": random.sample(proxList, k=1)[0]}
            else:
                proxies = {}
            adapter = SSLContextAdapter()
            req.mount(SESSION_URL, adapter)
            req.get(SESSION_URL, proxies=proxies, timeout=(5, 5), verify=True)
            getSession = False
            logging.info("get New Session")
            statics.set(stockName, sname, "NEW_SESSION")
        except BaseException as e:
            logging.error("get Session Exception :" + str(e))
            statics.set(stockName, sname, "SESSION_ERROR")
            if not chkRun(0):
                sys.exit(0)
            for i in range(10 * 60):
                lookStop()
                time.sleep(1)


getNewSession()
while run:
    lookStop()
    sleep = 30  # 間隔30秒
    lookStop()
    b = time.time()
    stock = twstock.realtime.get(stockCodeL, req, proxies, logging)
    # print(runGroupStr,stock["success"])
    if stock["success"]:
        logging.debug("    success")
        # 轉換格式
        statics.set(stockName, sname, "SUCCESS")
        logcnt = 0
        for code, v in stock.items():
            logcnt = logcnt + 1
            if isinstance(v, dict) and v['success']:
                try:
                    del v['info']
                    rlTime = v['realtime']
                    del v['realtime']
                    v.update(rlTime)
                    v.update({'group': group[v['code']][0:2]})
                    # 存入db
                    # collRT.insert_one(v)
                    # 新的訊息有可能沒有交易，新增一筆的方式是要張數有增加
                    query = {"code": v['code'], "date": v['date'], "accumulate_trade_volume": {
                        "$gte": v['accumulate_trade_volume']}}
                    value = {"$set": v}
                    if logcnt == 1:
                        logging.debug("        db inst beg")

                    if "final_trade_volume" not in v:
                        if logcnt == 1:
                            logging.debug("        " + str({"accumulate_trade_volume": v['accumulate_trade_volume'], "trade_volume": v['trade_volume']})
                                          )
                        collRT.update_one(query, value, upsert=True)
                    else:
                        query = {"code": v['code'], "date": v['date'],
                                 "final_trade_volume": v['final_trade_volume']}
                        if logcnt == 1:
                            logging.debug(
                                "        " + str({"final_trade_volume": v['final_trade_volume'], "trade_volume": v['trade_volume']}))
                        value = {"$set": v}
                        collRT.update_one(query, value, upsert=True)

                    if logcnt == 1:
                        logging.debug("        db inst end")
                except BaseException as e:
                    logging.error("    BaseException :" + str(e))
    else:
        statics.set(stockName, sname, "ERROR")
        logging.error("    realtime error: " + stock['rtmessage'])
        getNewSession()
        proxies = {"http": random.sample(proxList, k=1)[0]}
    """
    #查詢股票群組
    for stockGroupCode,codeL in group.items():
        #取得股票即時資料
        b = int(time.mktime(time.localtime()))
        stock = twstock.realtime.get(codeL)
        if stock["success"]:
            #轉換格式
            for code, v in stock.items():
                if isinstance(v, dict):
                    del v['info']
                    rlTime = v['realtime']
                    del v['realtime']
                    v.update(rlTime)
                    v.update({'group':stockGroupCode})
                    #存入db
                    #collRT.insert_one(v)
                    query = {"code":v['code'],"timestamp":v['timestamp']}
                    value = { "$set": v }
                    collRT.update_one(query, value, upsert=True)
    e = localtime
    print(stockGroupCode, ":", e-b, flush=True)
    """
    run = chkRun(0)

    #localtime = int(time.mktime(time.localtime()))
    e = time.time()
    sleep = sleep - (e-b)  # 間隔時間含有執行時間
    if sleep > 0:
        time.sleep(sleep)
    #print("===" + time.ctime() + "===", e-b, flush=True)
else:
    logging.info("time out")
# print(time.ctime());
"""
python3 stock.py TWSE 01,02,20
python3 stock.py TWSE 03,21,12
python3 stock.py TWSE 04,18,14
python3 stock.py TWSE 28
python3 stock.py TWSE 05,22
python3 stock.py TWSE 06,08,09
python3 stock.py TWSE 10,11
python3 stock.py TWSE 15,25
python3 stock.py TWSE 24
python3 stock.py TWSE 31,27
python3 stock.py TWSE 26,29,39
python3 stock.py TWSE 23,16,17
"""
