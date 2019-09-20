#coding=utf-8
import requests
import os
import sys
import re
import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import lxml
from lxml import etree
import uuid
import argparse 
import subprocess
reload(sys)

sys.setdefaultencoding('utf-8')


pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules import SpyderUtils
from modules import FileUtils
from modules import CollectionUtils,RexUtils, InteractUtils,ThreadUtils


if __name__ == "__main__":

    for i in range(0,15):
        ri = 27-i
        cmd = 'python androidSDKSpy.py -e {}'.format(ri)
        print cmd
        ThreadUtils.execute_command(cmd,debug=True)
        # subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        # os.popen(cmd)
        print 'sdk-{} done!'.format(ri)