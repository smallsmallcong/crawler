#-*-coding:utf-8 -*-

import pandas as pd
import requests
import json
import os
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

file = pd.read_csv('areaid.csv')
tot  = len(file['NAMEEN'])

url_base = 'http://service.envicloud.cn:8082'

stime = 2020011104
etime = 2020011202

while stime <= etime:

    print stime

    update = []
    cityname = []
    stationname = []
    aqi = []
    pm25 = []
    pm10 = []
    o3 = []
    so2 = []
    no2 = []
    co = []

    num = 0

    while num < tot:

        citycode = file['AREAID'][num]

        try:

            url = url_base+'/v2/air/hourly/city/U1NTTEXLMTQ1OTM5MJK5NDGWNA==/'+str(citycode)+'/'+str(stime)
            res = requests.get(url)
            obs = json.loads(res.text)
            obs = json.dumps(obs,encoding='UTF-8',ensure_ascii=False)
            obs = eval(obs)

            info = obs['info']

            tot_info = len(info)

            info_num = 0

            while info_num < tot_info:

                update.append(obs['time'])
                cityname.append(obs['cityname'])
                stationname.append(info[info_num]['stationname'])
                aqi.append(info[info_num]['AQI'])
                pm25.append(info[info_num]['PM25'])
                pm10.append(info[info_num]['PM10'])
                o3.append(info[info_num]['o3'])
                so2.append(info[info_num]['SO2'])
                no2.append(info[info_num]['NO2'])
                co.append(info[info_num]['CO'])

                info_num = info_num + 1

            num = num + 1

        except:

            num = num + 1

    update = pd.Series(update)
    cityname = pd.Series(cityname)
    stationname = pd.Series(stationname)
    aqi = pd.Series(aqi)
    pm25 = pd.Series(pm25)
    pm10 = pd.Series(pm10)
    o3 = pd.Series(o3)
    so2 = pd.Series(so2)
    no2 = pd.Series(no2)
    co = pd.Series(co)

    data = pd.concat([update,cityname,stationname,aqi,pm25,pm10,o3,so2,no2,co],axis=1,keys=['time','cityname','stationname','aqi','pm25','pm10','o3','so2','no2','co'])
    data.to_csv('obs_allstations_'+str(stime)[:8]+'_'+str(stime)[8:]+'.csv',index=False)

    stime = str(stime)
    stime = datetime.datetime.strptime(stime,'%Y%m%d%H')
    stime = stime+datetime.timedelta(hours=1)
    stime = datetime.datetime.strftime(stime,'%Y%m%d%H')
    stime = int(stime)












