import os
import sys
import subprocess
import logging
logging.basicConfig()

pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules.FileUtils import *
from modules.InteractUtils import *
from modules.ApkUtils import *

if __name__ == '__main__':
    pass
