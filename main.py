from icl import *
from tr import transform
import os

yaml.warnings({'YAMLLoadWarning': False})
globalConfiguration = {}

# 菜单
def mainMenu():
    print('==========================')
    print('1.数据管理')
    print('2.配置迁移')
    print('==========================')
    print('0.退出')
    print('==========================')
    print('请输入您的选择：')
    choice = input()
    return choice

def iclMenu():
    print('==========================')
    print('1.查询近10条日志')
    print('2.查询任务队列')
    print('==========================')
    print('0.返回')
    print('==========================')
    print('请输入您的选择：')
    choice = input()
    return choice

while True:
    choice = mainMenu()
    if choice == '1':
        os.system('cls')
        while True:
            icl = Icl()
            icl.initIcl()
            subChoice = iclMenu()
            if subChoice == '1':
                icl.showLog(1, 10)
            elif subChoice == '2':
                icl.showTaskList()
            elif subChoice == '0':
                break
        break
    elif choice == '2':
        os.system('cls')
        # 从输入读取start
        start = input('请输入需要转换的起始位置: ')
        # 从输入读取end
        end = input('请输入需要转换的终止位置: ')
        # 从输入读取old
        old = input('请输入需要转换的原始速通json: ')
        transform(start, end, old)
        break
    elif mainMenu() == '0':
        break