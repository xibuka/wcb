#coding=utf8
import itchat
import json
import requests

KEY = 'e4680558cea54262914cb2e68eea7149'    # change to your API KEY
url = 'http://www.tuling123.com/openapi/api'
headers = {'Content-type': 'text/html', 'charset': 'utf-8'}

# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息
@itchat.msg_register('Text')
def text_reply(msg):
    # 当消息不是由自己发出的时候
    if not msg['FromUserName'] == myUserName:
        # # 发送一条提示给文件助手
        # itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
        #                 (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
        #                  msg['User']['NickName'],
        #                  msg['Text']), 'filehelper')

        # 生成要求
        req_info = msg['Text'].encode('utf-8')
        query = {'key': KEY, 'info': req_info}

        # 取得回应
        r = requests.get(url, params=query, headers=headers)
        res = r.text

        # 回复给好友
        # return u'[自动回复]您好，我现在有事不在，一会再和您联系。\n已经收到您的的信息：%s\n' % (msg['Text'])
        return json.loads(res).get('text').replace('<br>', '\n')

if __name__ == '__main__':
    itchat.auto_login()

    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run()
