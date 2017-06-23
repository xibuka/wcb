#!/root/.pyenv/shims/python       
#-*- coding: UTF-8 -*-            
import itchat
import sys                        
import time                       
import threading

#TargetUserName="shibunkan"
TargetUserName="filehelper"

reply_box ={
        '8:0:0' :'起床了!起床了!起床了!',
        '12:0:0':'中午好好吃饭',
        '17:0:0':'我下班了，现在回家',
        }

@itchat.msg_register('Text')
def text_reply(msg):
    pass

def TimeTask():
    while True:

        for target_time, message in reply_box.items():
            th,tm,ts=target_time.split(':')

            current_time = time.localtime(time.time())

            if((current_time.tm_hour == int(th)) and 
               (current_time.tm_min  == int(tm)) and 
               (current_time.tm_sec  == int(ts))):
                itchat.send(message, toUserName=TargetUserName)

        time.sleep(1)

if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2)

    #TimeTask()
    positiveSendingThread = threading.Thread(target=TimeTask)
                                            # args=())
    positiveSendingThread.setDaemon(True)
    positiveSendingThread.start()

    itchat.run()
