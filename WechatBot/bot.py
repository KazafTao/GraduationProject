# -*- coding: utf-8 -*-
import os
import threading

import django
import itchat
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

# os.environ.setdefault('DJANGO_SETTING_MODULE', 'GraduationProject.settings')
# django.setup()

# from emoji.models import User


def search(keyword):
    es = Elasticsearch(hosts=["120.77.148.37"])
    search = Search(using=es, index='emoji', doc_type='emojis')
    res = search.query('match', type=keyword)[:4].execute()
    dict = res.to_dict()['hits']['hits']
    result = []
    for item in dict:
        result.append(item['_source']['path'])

    return result


# def sendEmoji(msg):
#     dir = '../GraduationProject/Crawler/Crawler/datas/emoji'
#     images = search(msg['Content'])
#     if images:
#         for image in images:
#             itchat.send_image(dir + '/' + image, msg['FromUserName'])
#     else:
#         itchat.send_msg('没找到喔(´ﾟдﾟ`)', toUserName=msg['FromUserName'])


# def bindEmail(email, wechat):
#     user = User.objects.get(email=email)
#     if user:
#         user.wechat = wechat
#         user.save()
#         return user.username + "绑定成功"
#     else:
#         return "该邮件地址还未注册"


def getEmojiByEmail(email):
    dir = "../GraduationProject/Crawler/Crawler/datas/userEmojis"
    return os.listdir('%s/%s' % (dir, email))


# 回复信息
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # if '绑定' in msg['Content']:
    #     email = msg['Content'][2:]
    #     print("email : " + email)
    #     itchat.send_msg(bindEmail(email, msg['FromUserName']),
    #                     toUserName=msg['FromUserName'])
    #     return

    if '教程' == msg['Content']:
        itchat.send_msg("回复绑定+邮箱地址即可绑定账号",
                        toUserName=msg['FromUserName'])
        itchat.send_msg("如：绑定white.mr@qq.com",
                        toUserName=msg['FromUserName'])
        itchat.send_msg("回复任意内容即以此为关键字搜索相应表情包",
                        toUserName=msg['FromUserName'])
        itchat.send_msg("如：小姐姐",
                        toUserName=msg['FromUserName'])
        return

    # if '我的表情' == msg['Content']:
    #     user = User.objects.get(wechat=msg['FromUserName'])
    #     if user:
    #         itchat.send_msg("your email : " + user.email,
    #                         toUserName=msg['FromUserName'])
    #         dir = "../GraduationProject/Crawler/Crawler/datas/userEmojis"
    #         emojis = getEmojiByEmail(user.email)
    #         for emoji in emojis:
    #             itchat.send_image('%s/%s/%s' % (dir, user.email, emoji), toUserName=msg['FromUserName'])
    #     return
    #
    # sendEmoji(msg)


@itchat.msg_register(itchat.content.FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])  # 自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Hi( •̀ ω •́ )✧',
                    msg['RecommendInfo']['UserName'])
    itchat.send_image('welcome.png', msg['RecommendInfo']['UserName'])
    itchat.send_msg('回复 教程 了解一下',
                    msg['RecommendInfo']['UserName']),


print('thread %s is runing' % threading.current_thread().name)
# 在linux上要设置enableCmdQR=2
itchat.auto_login(True)
itchat.run()
