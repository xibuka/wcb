#!/root/.pyenv/shims/python       
#-*- coding: UTF-8 -*-            
import itchat
import requests
import sys                        
import time                       
import json                       
import geoip2.webservice
import _thread, threading
from bs4 import BeautifulSoup     
from pygeocoder import Geocoder, GeocoderResult

KEY = 'e4680558cea54262914cb2e68eea7149'    # change to your API KEY
url = 'http://www.tuling123.com/openapi/api'
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

    #print(url)
    #print(parsed_json)
    #print("Current temperature in %s is: %s" % (city_name, temp_c))

    return("现在时间 %s, %s 气温 %s 摄氏度。%s" % (current_time, city_name, temp_c, summary))

# auto reply if the message is Text
@itchat.msg_register('Text')
def text_reply(msg):

    # add/remove user to chat list when he/she want to chat or quit
    if   msg['Text'] == chatStart:
        chatUsersList.append(msg['FromUserName'])
        return(chatStartMsg)
    elif msg['Text'] == chatEnd:
        chatUsersList.remove(msg['FromUserName'])
        return(chatEndMsg)
    elif translateStart in msg['Text'] :
        word=msg['Text'].replace(translateStart,'',1)
        return(TransToEn(word))
    elif weatherStart in msg['Text'] :
        weatherTargetPlace=msg['Text'].replace(weatherStart,'',1)
        return(WeatherSummary(weatherTargetPlace))
    else:
        pass

    # chat to user when he/she is in the chatUsersList
    if msg['FromUserName'] in chatUsersList:
        # backup msg to filehelper
        itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                        (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                         msg['User']['NickName'], msg['Text']), 'filehelper')

        #WeatherSummary(city_name)

        # make query 
        query = {'key':  KEY, 
                 'info': msg['Text'].encode('utf-8')}

        # get response
        res = requests.get(url, params=query, headers=headers).text

        # reply
        return json.loads(res).get('text').replace('<br>', '\n')

if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2)

    # get own UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]

    itchat.run()
