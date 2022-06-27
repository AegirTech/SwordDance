#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email import header
import requests
import json
import yaml
yaml.warnings({'YAMLLoadWarning': False})
class Icl:
    
    globalConfiguration = {}

    def initIcl(self):
        # 初始化./config.yml文件到全局变量globalConfiguration，若其不存在，立即创建
        try:
            with open('./config.yml', 'r') as f:
                self.globalConfiguration = yaml.safe_load(f)
        except FileNotFoundError:
            with open('./config.yml', 'w') as f:
                yaml.dump(self.globalConfiguration, f)

        # 检查是否配置url，若没有配置，从输入读取，并保存到./config.yml文件
        if 'url' not in self.globalConfiguration:
            self.globalConfiguration['url'] = input('请输入url: ')
            with open('./config.yml', 'w') as f:
                yaml.dump(self.globalConfiguration, f)
        print(self.globalConfiguration['url'])
        if 'username' not in self.globalConfiguration:
            self.globalConfiguration['username'] = input('请输入用户名: ')
            self.globalConfiguration['password'] = input('请输入密码: ')
            with open('./config.yml', 'w') as f:
                yaml.dump(self.globalConfiguration, f)
        print("pass")
        if 'token' not in self.globalConfiguration:
            self.login()
        elif self.isLoginOverdue():
            self.login()
        else:
            print("欢迎回来")

    # 登陆函数
    def login(self):
        print(self.globalConfiguration['url'])
        res = requests.post(
                self.globalConfiguration['url'] + '/adminLogin',
                data={
                    'username': self.globalConfiguration['username'], 
                    'password': self.globalConfiguration['password']
                }
            )

        if res.ok:
            self.globalConfiguration['token'] = res.json()['data']['token']
            print("欢迎回来")

        with open('./config.yml', 'w') as f:
            yaml.dump(self.globalConfiguration, f)

    # 判断登陆是否过期
    def isLoginOverdue(self):
        # 通过GET请求/showLog的current=1，size=1，查看状态码是否为401判断token是否有效，若返回401则无效，重新请求token
        r = requests.get(self.globalConfiguration['url'] + '/showLog',
                         params={'current': 1, 'size': 1},
                         headers={'Authorization': "Bearer "+self.globalConfiguration['token']},
                         verify=False
                         )
        if r.status_code == 401:
            return True
        elif r.status_code == 200:
            return False

    # log查询
    def showLog(self,current, size):
        # 通过GET请求/showLog的current=1，size=1
        r = requests.get(self.globalConfiguration['url'] + '/showLog',
                         params={'current': current, 'size': size},
                         headers={'Authorization': "Bearer "+self.globalConfiguration['token']})
        data = r.json()['data']
        for x in data:
            log = str(x['id']) + '\t' + x['level']+'\t' + x['taskType']+'\t' + \
                x['title']+'\t'+x['from']+'\t'+str(x['name'])+'\t'+x['time']
            print(log)
        return r.ok

    # 任务队列
    def showTaskList(self):
        # 通过GET请求/showFreeTaskList
        r = requests.get(self.globalConfiguration['url'] + '/showFreeTaskList',
                         headers={'Authorization': "Bearer "+self.globalConfiguration['token']}
                         )
        data = r.json()['data']
        print("任务列表")
        for account in data:
            print(account['name']+"\t"+account['taskType'] +
                  "\t"+str(account['server']))

    # 载入设备查询
    def showLoadedDevice(self):
        # 通过GET请求/showLoadedDevice
        r = requests.get(self.globalConfiguration['url'] + '/showLoadedDevice',
                         headers={'Authorization': "Bearer "+self.globalConfiguration['token']})
        data = r.json()['data']
        print("已载入设备列表")
        for key in data:
            print(key+"\t"+str(data[key]))

    # 增加设备
    def addDevice(self):
        data = {
            "id": 0,
            "deviceName": "string",
            "deviceToken": "string",
            "expireTime": "2122-06-17T08:55:55.994Z",
            "delete": 0
        }
        # 从输入设置deviceName
        data['deviceName'] = input("设备名称：")
        # 通过POST请求/addDevice
        r = requests.post(self.globalConfiguration['url'] + '/addDevice',
                          json=data, headers={'Authorization': "Bearer "+self.globalConfiguration['token']})
        print("新增设备: "+r.json()['data']['deviceToken'])

    # 增加账号
    def addAccount(self):
        data = {
            "id": 0,
            "name": "string",
            "account": "string",
            "password": "string",
            "server": 0,
            "taskType": "daily",
            "config": {
                "daily": {
                    "fight": [
                        {
                            "level": "1-7",
                            "num": 1
                        }
                    ],
                    "sanity": {
                        "drug": 0,
                        "stone": 0
                    },
                    "mail": True,
                    "offer": {
                        "enable": True,
                        "car": False,
                        "star4": True,
                        "star5": False,
                        "star6": False,
                        "other": False
                    },
                    "friend": True,
                    "infrastructure": {
                        "harvest": True,
                        "shift": True,
                        "acceleration": True,
                        "communication": True,
                        "deputy": False
                    },
                    "credit": True,
                    "task": True,
                    "activity": True
                },
                "rogue": {
                    "operator": {
                        "index": 0,
                        "num": 0,
                        "skill": 0
                    },
                    "level": 0,
                    "coin": 0,
                    "skip": {
                        "coin": True,
                        "beast": True,
                        "daily": True,
                        "sensitive": True,
                        "illusion": True,
                        "survive": True
                    }
                }
            },
            "expireTime": "2122-06-18T02:21:36.336Z",
            "delete": 0
        }
        # 从输入设置name
        data['name'] = input("账号名称：")
        # 从输入设置account
        data['account'] = input("账号：")
        # 从输入设置password
        data['password'] = input("密码：")

        # 通过POST请求/addAccount
        r = requests.post(self.globalConfiguration['url'] + '/addAccount',
                          json=data, headers={'Authorization': "Bearer "+self.globalConfiguration['token']})
        if r.ok:
            print("新增账号: "+data['account'])
        else:
            print("新增账号失败")