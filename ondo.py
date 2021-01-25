#-*- coding: utf-8 -*-

import json
import requests
import schedule
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
from datetime import datetime
import math


def dsmTest():

    # current date and time
    now = datetime.now() 
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H")
    nowTime = year + month + day + time


    # 공공데이터 API
    apiUrl = 'http://apis.data.go.kr/1360000/TourStnInfoService/getTourStnVilageFcst'
    key = unquote('FqafH8mStSoLSHj4Muzv0tHZ76RczPq5lkbH%2FkfN4XVCK7gko2SO6ZvYLrw9NeLIABSeJYmf8VFHBVB2G7dNDw%3D%3D')
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : key, quote_plus('pageNo') : '1', quote_plus('numOfRows') : '1', quote_plus('dataType') : 'JSON', quote_plus('CURRENT_DATE') : nowTime , quote_plus('HOUR') : '1', quote_plus('COURSE_ID') : '53' })
    request = Request(apiUrl + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    jsonLoader = json.loads(response_body)

    temper = jsonLoader['response']['body']['items']['item'][0]['th3']
    skyConditionJson = jsonLoader['response']['body']['items']['item'][0]['sky']
    skyCondition = ''

    # print(jsonLoader)
    temper = jsonLoader['response']['body']['items']['item'][0]['th3']

    # 835e3cffb5f0b27e8e3bcce876722503

    # openWeather API
    weathreApiUrl = 'http://api.openweathermap.org/data/2.5/weather'
    weathreApiKey = unquote('835e3cffb5f0b27e8e3bcce876722503')
    queryParams = '?' + urlencode({ quote_plus('q') : 'Seoul', quote_plus('appid') : weathreApiKey })
    weatherRequest = Request(weathreApiUrl + queryParams)
    weatherRequest.get_method = lambda: 'GET'
    weather_response_body = urlopen(weatherRequest).read()
    weatherJsonLoader = json.loads(weather_response_body)
    
    ondo = weatherJsonLoader['main']['temp'] - 273.15
    lastOndo = math.trunc(ondo)

    if skyConditionJson == 1:
        skyCondition = '맑음'
    elif skyConditionJson == 2:
        skyCondition = '구름조금'
    elif skyConditionJson == 3:
        skyCondition = '구름많음'
    elif skyConditionJson == 4:
        skyCondition = '흐림'
    elif skyConditionJson == 5:
        skyCondition = '비'
    elif skyConditionJson == 6:
        skyCondition = '비눈'
    elif skyConditionJson == 7:
        skyCondition = '눈비'
    else:
        skyCondition = '눈'

    
    #ChatBot
    host = 'https://ifcommunity.synology.me/webapi/entry.cgi'
    string = '오늘의 날씨는 ' + skyCondition + '\n' + '현재 기온은 ' + str(lastOndo) + '℃' + '\n' + '일 평균 3시간 기온은 ' + str(temper) + '℃ 입니다'
    payload =  {'text': string}
    json_string = json.dumps(payload)
    params = {'api' : 'SYNO.Chat.External', 'method' : 'incoming', 'version' : '2', 'token' : 'kRdC6h0ZPbtsPoYnqKJRFgg3ZIGrjqhGENTtYmF6z3BcGFLlmdeBBLrEzf79jph5', 'payload' : json_string }
    res = requests.get(host, params=params)
    # jsonData = json.loads(res.content.decode('utf-8'))
    return res

now = datetime.now() 
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
time = now.strftime("%H")
nowTime = year + month + day + time
print(nowTime)
print("알림이 시작")

#월요일 
schedule.every().monday.at("08:00").do(dsmTest)
schedule.every().monday.at("17:30").do(dsmTest)
#화요일
schedule.every().tuesday.at("08:00").do(dsmTest)
schedule.every().tuesday.at("17:30").do(dsmTest)
#수요일
schedule.every().wednesday.at("08:00").do(dsmTest)
schedule.every().wednesday.at("17:30").do(dsmTest)
#목요일
schedule.every().thursday.at("08:00").do(dsmTest)
schedule.every().thursday.at("17:30").do(dsmTest)
#금요일
schedule.every().friday.at("08:00").do(dsmTest)
schedule.every().friday.at("17:30").do(dsmTest)

while True:
    schedule.run_pending()
    

