#!/usr/bin/python      
#-*- coding: UTF-8 -*- 

from wxpy import *
import requests
import sys                        
import time                       
import json                       
import geoip2.webservice
import _thread, threading
from bs4 import BeautifulSoup     
from pygeocoder import Geocoder, GeocoderResult

import doutu
from tempfile import NamedTemporaryFile

headers = {'Content-type': 'text/html', 'charset': 'utf-8'}

LANG="CN" #EN,CN,JP https://www.wunderground.com/weather/api/d/docs?d=language-support

hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}]

chatUsersList=[]
chatStart="开始聊天"
chatStartMsg="你好，我是shiri，咱们唠点什么？"
chatEnd="886"
chatEndMsg="拜拜 :)"
translateStart="翻译"
weatherStart="天气"
douTuStart="斗图"

TULING_APIKEY = 'e4680558cea54262914cb2e68eea7149'    # change to your API KEY
# 初始化图灵机器人
tulingrobot = Tuling(api_key=TULING_APIKEY)


# 登录
bot = Bot(console_qr=True, cache_path=True)


def TransToEn(city_name):
    url  = "https://translate.google.com/m?sl=auto&tl=en&ie=UTF-8&hl=en&q=" + city_name
    html = requests.get(url, headers=hds[0], allow_redirects=False, timeout=3)
    soup = BeautifulSoup(html.text.encode(html.encoding), "html.parser")
    return soup.find('div', {'class': 't0'}).text

def GetLocation(address):
    geocoder = Geocoder()
    try: 
        result = geocoder.geocode(address, language="en")
        return result.coordinates
    except Exception as e:
        return (None,None)

def WeatherSummary(city_name):

    city_name_en=TransToEn(city_name)
    (x,y) = GetLocation(city_name_en)

    if (x,y) == (None,None):
        return("Invaild input %s" % city_name)

    url = 'http://api.wunderground.com/api/33161f9ccca4985f/geolookup/conditions/forecast/'
    url = url + 'lang:' + LANG + '/q/'+str(x)+','+str(y)+'.json'
    r = requests.get(url, headers=hds[0], allow_redirects=False, timeout=3)

    parsed_json=r.json()
    location = parsed_json['location']['city']
    temp_c = parsed_json['current_observation']['temp_c']
    current_time=parsed_json['forecast']['txt_forecast']['date']

    summary=parsed_json['forecast']['txt_forecast']['forecastday'][0]['fcttext_metric']

    return("现在时间 %s, %s 气温 %s 摄氏度。%s" % (current_time, city_name, temp_c, summary))

def reply_doutu(msg,keyword):
    img_url=doutu.douTuLa(keyword)

    print(keyword, img_url)

    r = requests.get(img_url)

    tmp = NamedTemporaryFile()
    tmp.write(r.content)
    tmp.flush()

    media_id = bot.upload_file(tmp.name)
    msg.reply_image('.gif', media_id=media_id)
    tmp.close()

    return 

# 自动回复所有文字消息
@bot.register(msg_types=TEXT, except_self=False)
def reply_self(msg):

    chat_text = msg.text
    chat_sender = msg.sender.name
    chat_type = msg.type

    print( 'received: {} ({}) from {}'.format(msg.text, msg.type, msg.sender.name))

    # add/remove user to chat list when he/she want to chat or quit
    if   msg.text == chatStart:
        chatUsersList.append(chat_sender)
        return chatStartMsg
    elif msg.text == chatEnd:
        chatUsersList.remove(chat_sender)
        return chatEndMsg
    elif translateStart in msg.text :
        word=msg.text.replace(translateStart,'',1)
        return(TransToEn(word))
    elif weatherStart in msg.text :
        weatherTargetPlace=msg.text.replace(weatherStart,'',1)
        return(WeatherSummary(weatherTargetPlace))
    elif douTuStart in msg.text :
        keyword=msg.text.replace(douTuStart,'',1)
        return(reply_doutu(msg, keyword))
    else:
        pass

    # don't reply if chat is from group and not being @
    if isinstance(msg.chat, Group) and not msg.is_at:
        return
    
    # chat to user when he/she is in the chatUsersList
    if chat_sender in chatUsersList:
        tulingrobot.do_reply(msg)


@bot.register(msg_types=PICTURE, except_self=False)
def picture_reply(msg):
    print( 'received: {} ({}) from {}'.format(msg.text, msg.type, msg.sender.name))
    return
 
print("Ready to server")
# run
bot.join()
