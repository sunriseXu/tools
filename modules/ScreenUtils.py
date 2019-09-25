#coding=utf8
import os
import sys

import psutil
import ThreadUtils


def exeCmdList(cmdList,env={}):
    '''
    主要封装一个函数,提供一串命令,要么执行这条命令,并且获取返回值.要么发现正在运行,
    '''
    cmdResList = []
    for cmd in cmdList:
        #注意execute_command无法处理io密集任务，效率十分慢
        res = ThreadUtils.execute_command(cmd,env=env)
        cmdResList.append(res)
    return cmdResList

