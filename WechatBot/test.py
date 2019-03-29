import itchat, time, threading

@itchat.msg_register('Text')
def text_reply(msg):
    print(msg['Text'])
    print(msg.user)

def send_notification(nickName):
    memberList = itchat.search_friends(nickName = nickName)
    # if not full match, you may use this
    memberList = filter(lambda m: nickName in m['NickName'], itchat.get_contract()[1:])
    for member in memberList:
        itchat.send('Now the time is: ' + time.strftime(
            '%y%m%d-%H%M%S', time.localtime()), member['UserName'])
        time.sleep(.5)
    time.sleep(3)

itchat.auto_login(True)

positiveSendingThread = threading.Thread(target=send_notification,
    args=('\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0',))
positiveSendingThread.setDaemon(True)
positiveSendingThread.start()

itchat.run()