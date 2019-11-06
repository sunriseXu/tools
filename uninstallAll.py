import os
import sys
import time
import logging
import subprocess
from modules.InteractUtils import *
from modules.ThreadUtils import execute_command
from modules.FileUtils import *
from modules.AdbUtils import *


devices = getDevices()
devices = ['-s {} '.format(i) for i in devices]
for device in devices:
    uninstallAllThird(device,[])