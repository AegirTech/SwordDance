# 速通配置快速迁移工具
# 可以将速通的配置文件快速迁移到审判庭数据库中
# by DazeCake
import json
from operator import ne
import os

all = []

def transform(start,end,old):
    
    data = json.load(old)

    # 进行space[2]-space[1]+1次循环
    for index in range(start,end+1):
        print('=========================='+str(index)+'==========================')
        newData= {
        "id": 0,
        "name": "string",
        "account": "string",
        "password": "string",
        "server": 0,
        "taskType": "daily",
        "config": {
            "daily": {
                "fight": [
                ],
                "sanity": {
                    "drug": 0,
                    "stone": 0
                },
                "mail": True,
                "offer": {
                    "enable": True,
                    "car": True,
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
        "active": {
            "monday": {
                "enable": True,
                "detail": [

                ]
            },
            "tuesday": {
                "enable": True,
                "detail": [
                ]
            },
            "wednesday": {
                "enable": True,
                "detail": [
                ]
            },
            "thursday": {
                "enable": True,
                "detail": [
                ]
            },
            "friday": {
                "enable": True,
                "detail": [
                ]
            },
            "saturday": {
                "enable": True,
                "detail": [
                ]
            },
            "sunday": {
                "enable": True,
                "detail": [
                ]
            }
        },
        "expireTime": "2022-06-23T04:58:06.454Z",
        "delete": 0
    }
        print('username'+str(index))
        for key, value in data.items():
        # 遍历data中的每一个key包含“username”的value
            if 'username'+str(index) == key:
                print('username'+str(index))
                # 去除value中#号和后面的内容
                newData["account"] = value.split('#')[0]
                newData["name"] = value.split('#')[1]
                break
        for key, value in data.items():
            if 'server'+str(index) == key:
                newData["server"] = value
                break
        for key, value in data.items():
            if 'multi_account_user'+str(index)+'fight_ui' == key:
                newFight = value.split(' ')
                for fight in newFight:
                    # print(fight)
                    fightMap = {
                        "level": fight.split('*')[0],
                        "num": fight.split('*')[1]
                    }
                    newData["config"]["daily"]["fight"].append(fightMap)
                break
        for key, value in data.items():
             # 遍历data中的每一个key包含“password”的value
            if 'password'+str(index) == key:
                newData["password"] = value
                # 添加newData到all中
                all.append(newData.copy())
                break

    # 保存all到new.json文件以utf-8编码
    with open(os.path.join(os.path.dirname(__file__), 'new.json'), 'w', encoding='utf-8') as f:
        # 将all转换为json格式
        json.dump(all, f, ensure_ascii=False, indent=4)
