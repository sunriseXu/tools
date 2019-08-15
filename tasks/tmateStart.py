#coding=utf8
import os
import sys

import psutil

pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)
from datetime import datetime
from modules import ThreadUtils


def checkAlive(processName):
    aliveStatus = ['sleeping','running']
    pidList = psutil.pids()
    for pid in pidList:
        p = psutil.Process(pid)
        if processName in p.name() and p.status() in aliveStatus:
            return True
    return False


# 主要封装一个函数,提供一串命令,要么执行这条命令,并且获取返回值.要么发现正在运行,
def exeCmdList(cmdList,env):
    cmdResList = []
    for cmd in cmdList:
        res = ThreadUtils.execute_command(cmd,env=env)
        cmdResList.append(res)
    return cmdResList
def writeFileA(fileName,content):
    # print('enter %s' %fileName)
    with open(fileName,'a') as f:
        # print('append %s' %content)
        f.write(content)
        f.write('\n')
def startTmate():
    pass


if __name__ == '__main__':
    fileName = '/home/limin/Documents/jianguoyun/Nutstore/tmate.txt'
    yesterday = datetime.today()
    todayTime = yesterday.strftime('%Y-%m-%d')
    cmdList = [
        'tmate -S /tmp/tmate-{}.sock new-session -d'.format(todayTime),
        'tmate -S /tmp/tmate-{}.sock wait tmate-ready'.format(todayTime),
        "tmate -S /tmp/tmate-{}.sock display -p '#{{tmate_web}}'".format(todayTime),
    ]
    aliveRes = checkAlive('tmate')
    cmdRes = []
    new_env = os.environ.copy()
    if 'TMUX' in new_env:
        new_env.pop('TMUX')
    if 'ZSH' not in new_env:
        new_env.update({'SHELL': '/usr/bin/zsh'})
        new_env.update({'ZSH': '/home/limin/.oh-my-zsh'})
    print(new_env)
    if not aliveRes:
        cmdRes = exeCmdList(cmdList, new_env)
        cmdRes = [' '.join(cmd.strip().split()) for cmd in cmdRes]
        print(cmdRes)
        writeFileA(fileName, '####### {} #######'.format(todayTime))
        for cmd in cmdRes:
            writeFileA(fileName, cmd)
