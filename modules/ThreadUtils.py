#coding=utf-8
import io
import json
import argparse 
import os
import sys
import subprocess
import time
import multiprocessing
import threading
import datetime
import logging
import re

logging.basicConfig()
l = logging.getLogger("ThreadUtils")

class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

def execute_command(cmdstring, timeout=None,env=None, debug=False):
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    try:
        sub = None
        if not env:
            sub = subprocess.Popen(cmdstring,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        else:
            sub = subprocess.Popen(cmdstring, shell=True,env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except OSError:
        return 'OSError'
    while True:
        if sub.poll() is not None:
            break
        time.sleep(0.1)
        # print 'poll is none'
        if debug:
            buff = sub.stdout.readline()
            print(buff)
        if timeout:
            if end_time <= datetime.datetime.now():
                try:
                    sub.kill()
                except Exception,e:
                    return "TIME_OUT"
                return "TIME_OUT"
    res=sub.stdout.read()
    if sub.stdin:
        sub.stdin.close()
    if sub.stdout:
        sub.stdout.close()
    if sub.stderr:
        sub.stderr.close()
    try:
        sub.kill()
    except OSError:
        return res
    return res