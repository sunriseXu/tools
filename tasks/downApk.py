#coding=utf8
import os
import sys

import psutil

pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)
from datetime import datetime
from modules import ThreadUtils
from datetime import datetime,timedelta

def checkAlive(processName):
    aliveStatus = ['sleeping','running']
    pidList = psutil.pids()
    for pid in pidList:
        p = psutil.Process(pid)
        if processName in p.name() and p.status() in aliveStatus:
            return True
    return False
zshEnv = {
    'LESS': '-R',
    'LC_CTYPE': 'en_US.UTF-8',
    'XDG_SESSION_TYPE': 'x11',
    'LC_PAPER': 'zh_CN.UTF-8',
    'VIRTUALENVWRAPPER_SCRIPT': '/usr/local/bin/virtualenvwrapper.sh',
    'SHELL': '/usr/bin/zsh',
    'XDG_DATA_DIRS': '/usr/share/ubuntu:/usr/share/gnome:/usr/local/share:/usr/share:/var/lib/snapd/desktop', 'MANDATORY_PATH': '/usr/share/gconf/ubuntu.mandatory.path', 'CLUTTER_IM_MODULE': 'xim', 'JOB': 'dbus', 'SESSION': 'ubuntu', 'XMODIFIERS': '@im=fcitx', 'JAVA_HOME': '/usr/lib/jvm/jdk1.8.0_201', 'GTK2_MODULES': 'overlay-scrollbar', 'WORKON_HOME': '/home/limin/Envs', 'XDG_RUNTIME_DIR': '/run/user/1000', 'LC_ADDRESS': 'zh_CN.UTF-8', 'J2SDKDIR': '/usr/lib/jvm/jdk1.8.0_201', 'XDG_SESSION_ID': 'c2', 'DBUS_SESSION_BUS_ADDRESS': 'unix:abstract=/tmp/dbus-GUlBWFhpHi', 'DEFAULTS_PATH': '/usr/share/gconf/ubuntu.default.path', 'DESKTOP_SESSION': 'ubuntu', 'GTK_MODULES': 'gail:atk-bridge:unity-gtk-module', 'INSTANCE': '', 'LC_NAME': 'zh_CN.UTF-8', 'XDG_MENU_PREFIX': 'gnome-', 'LS_COLORS': 'rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:', 'LC_NUMERIC': 'zh_CN.UTF-8', 'GNOME_DESKTOP_SESSION_ID': 'this-is-deprecated', 'XDG_CURRENT_DESKTOP': 'Unity', 'USER': 'limin', 'XDG_VTNR': '7', 'XAUTHORITY': '/home/limin/.Xauthority', 'LANGUAGE': 'en_US:en', 'SESSION_MANAGER': 'local/limin:@/tmp/.ICE-unix/4293,unix/limin:/tmp/.ICE-unix/4293', 'LC_MEASUREMENT': 'zh_CN.UTF-8', 'QT_QPA_PLATFORMTHEME': 'appmenu-qt5', 'QT_ACCESSIBILITY': '1', 'WINDOWID': '77594634', 'GPG_AGENT_INFO': '/home/limin/.gnupg/S.gpg-agent:0:1', 'LANG': 'en_US.UTF-8', 'GDMSESSION': 'ubuntu', 'XDG_SEAT_PATH': '/org/freedesktop/DisplayManager/Seat0', '_': '/usr/bin/python', 'GTK_IM_MODULE': 'fcitx', 'XDG_CONFIG_DIRS': '/etc/xdg/xdg-ubuntu:/usr/share/upstart/xdg:/etc/xdg', 'LC_TIME': 'zh_CN.UTF-8', 'PAGER': 'less', 'XDG_GREETER_DATA_DIR': '/var/lib/lightdm-data/limin', 'QT4_IM_MODULE': 'fcitx', 'HOME': '/home/limin', 'DISPLAY': ':1', 'XDG_SESSION_DESKTOP': 'ubuntu', 'LC_MONETARY': 'zh_CN.UTF-8', 'QT_LINUX_ACCESSIBILITY_ALWAYS_ON': '1', 'LC_IDENTIFICATION': 'zh_CN.UTF-8', 'VTE_VERSION': '4205', 'UPSTART_SESSION': 'unix:abstract=/com/ubuntu/upstart-session/1000/4042', 'GNOME_KEYRING_PID': '', 'CHROME_REMOTE_DESKTOP_DEFAULT_DESKTOP_SIZES': '1920x1080', 'VIRTUALENVWRAPPER_HOOK_DIR': '/home/limin/Envs', 'PAPERSIZE': 'a4', 'J2REDIR': '/usr/lib/jvm/jdk1.8.0_201', 'TMUX_PANE': '%3', 'QT_IM_MODULE': 'fcitx', 'LOGNAME': 'limin', 'XDG_SEAT': 'seat0', 'GNOME_KEYRING_CONTROL': '', 'PATH': '/home/limin/bin:/home/limin/.local/bin:/home/limin/android-studio/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/lib/jvm/jdk1.8.0_201/bin:/home/limin/Android/Sdk/tools:/home/limin/Android/Sdk/platform-tools:/home/limin/010editor:/home/limin/010editor:/home/limin/Android/Sdk/build-tools/28.0.3:/home/limin/Android/Sdk/platform-tools/:/home/limin/dex2jar-2.0:/opt/gradle/gradle-5.2.1/bin:/usr/lib/jvm/jdk1.8.0_201/bin:/home/limin/010editor:/home/limin/Android/Sdk/build-tools/28.0.3:/home/limin/Android/Sdk/platform-tools/:/home/limin/dex2jar-2.0:/opt/gradle/gradle-5.2.1/bin:/usr/lib/jvm/jdk1.8.0_201/bin', 'ZSH': '/home/limin/.oh-my-zsh', 'TERM': 'screen', 'VIRTUALENVWRAPPER_WORKON_CD': '1', 'XDG_SESSION_PATH': '/org/freedesktop/DisplayManager/Session0', 'COMPIZ_CONFIG_PROFILE': 'ubuntu', 'SESSIONTYPE': 'gnome-session', 'IM_CONFIG_PHASE': '1', 'SSH_AUTH_SOCK': '/run/user/1000/keyring/ssh', 'VIRTUALENVWRAPPER_PROJECT_FILENAME': '.project', 'GRADLE_HOME': '/opt/gradle/gradle-5.2.1', 'LSCOLORS': 'Gxfxcxdxbxegedabagacad', 'OLDPWD': '/home/limin/Desktop/mygit/tools', 'GDM_LANG': 'en_US', 'LC_TELEPHONE': 'zh_CN.UTF-8', 'SHLVL': '2', 'PWD': '/home/limin/Desktop/mygit/tools'
}

# 主要封装一个函数,提供一串命令,要么执行这条命令,并且获取返回值.要么发现正在运行,
def exeCmdList(cmdList,env={}):
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
    yesterday = datetime.today()#+ timedelta(-1)
    currTime = yesterday.strftime('%Y-%m-%d')
    cmdList = [
        'screen -dmS downApk-{}'.format(currTime),
        'screen -S downApk-{} -X stuff '\
        '"python3 /home/limin/Desktop/mygit/tools/spyder/huaweiSpy.py&&'\
        'python3 /home/limin/Desktop/mygit/tools/spyder/downloadApk.py\n"'.format(currTime),
    ]
    print(cmdList)
    res = exeCmdList(cmdList, zshEnv)












