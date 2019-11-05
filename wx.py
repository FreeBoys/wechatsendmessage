#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request,urllib.error,json
import sys

class WeChat(object):
        __token_id = ''
        # init attribute
        def __init__(self,url):
                self.__url = url.rstrip('/')
                self.__corpid = '[企业号的标识]'
                self.__secret = '[管理组凭证密钥]'

        # Get TokenID
        def authID(self):
                params = {'corpid':self.__corpid, 'corpsecret':self.__secret}
                data = urllib.parse.urlencode(params)

                content = self.getToken(data)

                try:
                        self.__token_id = content['access_token']
                        # print content['access_token']
                except KeyError:
                        raise KeyError

        # Establish a connection
        def getToken(self,data,url_prefix='/'):
                url = self.__url + url_prefix + 'gettoken?'
                try:
                        response = urllib.request.Request(url + data)
                except KeyError:
                        raise KeyError
                result = urllib.request.urlopen(response)
                content = json.loads(result.read())
                return content

        # Get sendmessage url
        def postData(self,data,url_prefix='/'):
                url = self.__url + url_prefix + 'message/send?access_token=%s' % self.__token_id
                request = urllib.request.Request(url,data.encode())
                print(url)
                print(data)
                try:
                        result = urllib.request.urlopen(request)
                except urllib.error.HTTPError as e:
                        if hasattr(e,'reason'):
                                print('reason',e.reason)
                        elif hasattr(e,'code'):
                                print('code',e.code)
                        return 0
                else:
                        content = json.loads(result.read())
                        result.close()
                return content

        # send message
        def sendMessage(self,touser,message):

                self.authID()

                data = json.dumps({
                        'touser':"[企业号中的用户帐号]",
                        'toparty':"[企业号中的部门id]",
                        'msgtype':"[消息类型]",
                        'agentid':"[企业号中的应用id]",
                        'text':{
                                'content':message
                        },
                        'safe':"0"
                },ensure_ascii=False)

                response = self.postData(data)
                print(response)


if __name__ == '__main__':
        a = WeChat('https://qyapi.weixin.qq.com/cgi-bin')
        a.sendMessage(sys.argv[1],sys.argv[3])
