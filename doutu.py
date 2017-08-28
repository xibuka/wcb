#!/usr/bin/python       
#-*- coding: UTF-8 -*-            
import requests
import sys
import time
import random
from bs4 import BeautifulSoup     

hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}]

def douTuLa(keyword):

    tuList=[]

    res = requests.get('https://www.doutula.com/search', {'keyword': keyword}, \
                            headers=hds[0], allow_redirects=False, timeout=5)

    if res.status_code == 200:

        soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")

        pic_block=soup.find('div', {'class': 'random_picture'})
   
        for img in pic_block.find_all('img'):
            img_url=img.get('data-original')
            if img_url != None :
                tuList.append('http:' + img_url)
    else:
        print(res.status_code)

    return random.choice(tuList)
