#coding=utf-8
import io
import json
import os
import sys
import time
import xml.dom.minidom as xmldom
import logging
import Levenshtein
import random
import re
logging.basicConfig()
l=logging.getLogger("xmlTest")


class Package:
    def __init__(self, pkgName):
        self.pkgName=pkgName
        self.activities=[]
        self.currentActivity=None
    def getAcitvity(self):
        return self.activities 
    def launchApp(self):
        startAppCmd="adb shell monkey -p %s -c android.intent.category.LAUNCHER 1" %self.pkgName
        os.popen(startAppCmd)
        time.sleep(2)
    def appendActivity(self,activity):
        if activity not in self.activities:
            self.activities.append(activity)
    def keepAlive(self):
        cPkg,_=self.getCurrentActivity()
        if self.pkgName not in cPkg:
            l.warning("current activity is not belong to package, try to resume")
            self.launchApp()
    def forward(self):
        self.currentActivity.forward()
        return
    def printInfo(self):
        print("packageName:%s" %self.pkgName)
        for activity in self.activities:
            activity.printInfo()
        return
    def dump(self):
        pkg,acti=Package.getCurrentActivity()
        while pkg not in self.pkgName:
            self.keepAlive()
            pkg,acti=Package.getCurrentActivity()
        newActFlag=True
        for activity in self.activities:
            # print activity.getActStr()
            if acti in activity.getActStr():
                newActFlag=False
                self.currentActivity=activity
                break
        if newActFlag:
            self.currentActivity=Acitivity(acti)
            self.activities.append(self.currentActivity)
        l.warning("dump current activity: %s" %acti)
        self.currentActivity.dump()

    @staticmethod
    def calculateSpace(str):
        if not str:
            return 0
        orilen=len(str)
        striplen=len(str.lstrip())
        return orilen-striplen

    @staticmethod
    def getCurrentActivity():
        activityCmd='adb shell "dumpsys activity activities|grep realActivity"'
        actStr=os.popen(activityCmd).read()
        actStr=actStr.split('\n')
        candidate=[]
        pIndent=Package.calculateSpace(actStr[0])
        for i in range(len(actStr)):
            cIndent=Package.calculateSpace(actStr[i+1])
            if cIndent>pIndent:
                if actStr[i+1].strip() not in candidate:
                    candidate.append(actStr[i+1].strip())
            else:
                break
        actStr=candidate[0]
        subStr=actStr.strip().split('=')[1]
        subStr=subStr.split('/')
        tup=(subStr[0],subStr[1])
        return tup

class Acitivity:
    def __init__(self, activity):
        self.activity=activity
        self.views=[]
        self.currentView=None
    def getActStr(self):
        return self.activity
    def printInfo(self):
        print("activityName:%s" %self.activity)
        idx=1
        lenViews=len(self.views)
        for view in self.views:
            print("No.%d/%d view:-------------" %(idx,lenViews))
            idx+=1
            view.printInfo()
        return
    def forward(self):
        self.currentView.forward()
    def checkNewView(self,view):
        newFlag=True
        for preview in self.views:
            dist=Levenshtein.distance(view.xmlStr,preview.xmlStr)
            # l.warning("Levenshtein distance:%d",dist)
            if dist == 0:
                newFlag=False
                self.currentView=preview
                break
        return newFlag
    def dump(self):   
        tmpView=View()
        tmpView.dump()
        if self.checkNewView(tmpView):
            self.currentView=tmpView
            self.views.append(tmpView)
            l.warning("new view found, new view is currentview")
        else:
            l.warning("old view is currentview")

class View:
    def __init__(self):
        self.xmltree=None
        self.xmlStr=None
        self.clickables={}
        self.randomClick=0
        

    def getXml(self):
        return self.xmltree
    def getXmlStr(self):
        return self.xmlStr
    def printInfo(self):
        # root=self.xmltree.documentElement
        # printTree(root,1)
        idx=1
        lenclick=len(self.clickables)
        for (key,value) in self.clickables.items():
            nodeName=key.nodeName
            className=key.getAttribute("class")
            text=key.getAttribute("text")
            print('<'+nodeName+' class:'+className+' text:'+text+' clicked:'+str(value)+'>')
    @staticmethod
    def trimXmlStr(xmlstr):
        c=re.compile(r"(?<=content-desc=).*?(?= checkable=)")
        ret=c.sub('" "',xmlstr,100)
        return ret
    # @profile
    def dump(self):
        UICmd='adb shell "uiautomator dump && cat /sdcard/window_dump.xml"'
        uixml=os.popen(UICmd).read()
        startIdx=uixml.find("<?xml")
        if startIdx:
            uixml=uixml[startIdx:]
            uixml=self.trimXmlStr(uixml)
            self.xmlStr=uixml
        else:
            l.error("indexError: cannot find xml string")
            return
        self.xmltree=xmldom.parseString(uixml)
        self.getClickable()
    def clickBound(self,element):
        midx,midy=self.getBound(element)
        clickCmd='adb shell input tap %s %s' %(str(midx),str(midy))
        l.warning(clickCmd)
        os.popen(clickCmd)
        return
    def getBound(self,element):
        allowxy=element.getAttribute("bounds")
        allowxy=allowxy.split("][")
        allowx=allowxy[0].strip('[')
        ltop=allowx.split(',')
        allowy=allowxy[1].strip(']')
        rbot=allowy.split(',')
        midx=int((int(ltop[0])+int(rbot[0]))/2)
        midy=int((int(ltop[1])+int(rbot[1]))/2)
        return (midx,midy)
    def setListView(self,root):
        for node in root.childNodes:
            className=node.getAttribute("class")
            if "TextView" in className:
                self.clickables.update({node:0})
            else:
                self.setListView(node)
    def getClickable(self):
        elementobj = self.xmltree.documentElement
        subElementObj = elementobj.getElementsByTagName("node")
        for element in subElementObj:
            clickable=element.getAttribute("clickable")
            midx,midy=self.getBound(element)
            if ("true" in clickable) and (midx+midy):
                self.clickables.update({element:0})
            className=element.getAttribute("class")
            if "ListView" in className:
                self.setListView(element)
        return
    def forward(self):
        doneFlag=True
        for (key,value) in self.clickables.items():
            if value==0:
                doneFlag=False
                self.clickBound(key)
                nodeName=key.nodeName
                className=key.getAttribute("class")
                text=key.getAttribute("text")
                l.warning('<'+nodeName+' class:'+className+' text:'+text+'>')
                self.clickables.update({key:1})
                time.sleep(1)
                break
        if doneFlag:
            if self.randomClick>len(self.clickables):
                l.warning("no clickable items anymore,click back")
                backCmd='adb shell input keyevent 4'
                os.popen(backCmd)
                
            else:
                l.warning("no clickable items anymore, random click")
                keyList=self.clickables.keys()
                rkey=random.choice(keyList)
                self.clickBound(rkey)
                self.randomClick+=1
            time.sleep(1)
        return doneFlag
    
    


def getSubString(myStr,myLen):
    if len(myStr)<myLen:
        return myStr
    else:
        return myStr[0:myLen]
def printNode(node,level,head):
    className=node.getAttribute("class")
    pkgName=node.getAttribute("package")
    clickable=node.getAttribute("clickable")
    if "true" in clickable:
        clickable=clickable+"++"
    nodeName=node.nodeName
    if head:
        prefix='<'
    else:
        prefix='</'
    if ("TextView" in className) or ("Button" in className) or("EditText" in className):
        text=node.getAttribute("text")
        text=getSubString(text,9)
        print(prefix+nodeName+' class:'+className+' clickable:'+clickable+' text:'+text+'>')
    else:
        print(prefix+nodeName+' class:'+className+' clickable:'+clickable+'>')
def printTree(root,level):
    className=root.getAttribute("class")
    head=True
    for i in range(level):
        print(" | "),
    printNode(root,level,head)
    head=False
    if(root.childNodes):
        for node in root.childNodes:
            printTree(node,level+1)
    for i in range(level):
        print(" | "),
    printNode(root,level,head)

def setListView(root):
    for node in root.childNodes:
        className=node.getAttribute("class")
        if "TextView" in className:
            print node.getAttribute("text")
        else:
            setListView(node)

def dumpXmlStr():
    UICmd='adb shell "uiautomator dump && cat /sdcard/window_dump.xml"'
    uixml=os.popen(UICmd).read()
    startIdx=uixml.find("<?xml")
    uixml=uixml[startIdx:]
    return uixml

def clickBound(element,selectedDevId):
    allowxy=element.getAttribute("bounds")
    allowxy=allowxy.split("][")
    allowx=allowxy[0].strip('[')
    ltop=allowx.split(',')
    allowy=allowxy[1].strip(']')
    rbot=allowy.split(',')
   
    midx=int((int(ltop[0])+int(rbot[0]))/2)
    midy=int((int(ltop[1])+int(rbot[1]))/2)
    
    clickCmd='adb'+selectedDevId+' shell input tap %s %s' %(str(midx),str(midy))
    res=os.popen(clickCmd)
    print res


def getUIXml(selectedDevId):
	UICmd='adb'+selectedDevId+' shell "uiautomator dump --compressed /sdcard/window_dump.xml >/dev/null && cat /sdcard/window_dump.xml"'
	uixml=os.popen(UICmd).read()
	if not uixml:
		return False
	domres=xmldom.parseString(uixml)
	elementobj = domres.documentElement
	subElementObj = elementobj.getElementsByTagName("node")
	resFlag=False
	for element in subElementObj:
		resId=element.getAttribute("resource-id")
		text=element.getAttribute("text")
		className=element.getAttribute("class")
		scrollable=element.getAttribute("scrollable")
		# focused=element.getAttribute("focused")
		if ("permission_allow_button" in resId) and ("ALLOW" in text):
			resFlag=True
			clickBound(element,selectedDevId)
			break
		elif ("ViewPager" in className) and ("true" in scrollable):
			resFlag=True
			# print "viewpaper found!"
			lswipeCmd='adb'+selectedDevId+' shell input swipe 1000 1500 200 1500'
			print os.popen(lswipeCmd)
			break	
	time.sleep(0.2)		
	return resFlag

def clickWelcome(selectedDevId):
	UICmd='adb'+selectedDevId+' shell "uiautomator dump --compressed /sdcard/window_dump.xml >/dev/null && cat /sdcard/window_dump.xml"'
	uixml=os.popen(UICmd).read()
	if not uixml:
		return False
	domres=xmldom.parseString(uixml)
	elementobj = domres.documentElement
	subElementObj = elementobj.getElementsByTagName("node")
	resFlag=False
	for element in subElementObj:
		clickable=element.getAttribute("clickable")
		if "true" in clickable:
			resFlag=True
			clickBound(element,selectedDevId)
			break
	return resFlag

if __name__ == "__main__":
   
    print("start to dump xmlstr1")
    uixml=dumpXmlStr()
    # print("tap to dump xmlstr2")
    # raw_input()
    # uixml2=dumpXmlStr()
    # print("Levenshtein distance between xmlstr1 and xmlstr2")
    # print("lenth of xmlstr1:%d" %len(uixml))
    # print("lenth of xmlstr2:%d" %len(uixml2))
    # print Levenshtein.distance(uixml,uixml2)
    # raw_input()
    uixml=View.trimXmlStr(uixml)
    xmlTree=xmldom.parseString(uixml) #xml字符串转xml对象
    # print xmlTree.toxml() xml对象转xml字符串
    # print(uixml)
    # raw_input()
    root=xmlTree.documentElement
    # print(root.nodeName)
    # print(root.nodeValue)
    # print(root.nodeType)
    # print(root.getElementsByTagName("node"))
    # print(root.childNodes)
    printTree(root,1)
    # sys.exit()

    subElementObj = root.getElementsByTagName("node")
    for element in subElementObj:
        className=element.getAttribute("class")
        if "ListView" in className:
            setListView(element)

    print("current pkg/act")
    print Package.getCurrentActivity()
    input()
    print("start")
    pk=Package("com.hanweb.gtzyb.jmportal.activity")
    pk.dump()
    print("tap to continue...")
    for i in range(100):
        pk.forward()
        pk.dump()
        # pk.printInfo()
        # print("tap to forward...")
        # raw_input()

