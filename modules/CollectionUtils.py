# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os
import json
import shutil
import sys
import logging
logging.basicConfig()
l = logging.getLogger("CollectionUtils")

def trimListItem(myList,unHeadStr='', unTailStr=''):
	'''
	trim list items, 'log_abc.txt' unHeadStr='log_' unTailStr='.txt' =>'abc'
	'''
	trimedList=[]
	for item in myList:
		if not item:
			continue
		res=item
		if unHeadStr and (unHeadStr in item):
			res=item.strip().split(unHeadStr)[1]
		if unTailStr and (unTailStr in item):
			res=res.strip().split(unTailStr)[0]
		trimedList.append(res)
	return trimedList

def graftListItem(myList, headStr='', tailStr=''):
	'''
	graft list items, 'abc' headStr='log_' tailStr='.txt' => 'log_abc.txt'
	'''
	graftedList=[]
	for item in myList:
		if not item:
			continue
		res=headStr + item + tailStr
		graftedList.append(res)
	return graftedList

def value2keylist(myValueList,mydict):
	'''
	mydict must have such form:{key:'value1',key2:'value2'} string:string
	and it's important that value in mydict should be unique too.
	get all keys according to their values, return key list
	'''
	resList=[]
	for item in myValueList:
		if not item:
			continue
		keyList=list(mydict.keys())
		valueList=list(mydict.values())
		try:
			idx=valueList.index(item)
			resList.append(keyList[idx])
		except ValueError:
			l.warning("%s in myValueList dont have matched value in mydict! use '-' to replace",item)
			resList.append('-')
	return resList

def key2Valuelist(myKeyList,mydict):
	'''
	mydict must have such form:{key:'value1',key2:'value2'} string:string
	get all values according to their key, return value list
	'''
	resList=[]
	for item in myKeyList:
		if not item:
			continue
		if item in mydict.keys():
			resList.append(mydict[item])
		else:
			l.warning("%s in myKeyList dont have matched key in mydict! use '-' to replace",item)
			resList.append('-')
	return resList

def appendDict(mydict,key,myValue):
	'''
	mydict must have such form: {key:[listItem1,listItem2]}
	dict type can be changed in function,while string,int, basic type can not 
	'''
	if key not in mydict.keys():
		mydict.update({key:myValue})
	return mydict

def dictMerge(*dicts):
    '''
    merge all dict in dicts, return merged dict. len(dicts)>=2
    '''
    if len(dicts)<2:
        l.warning("arguments must larger than one")
        return
    resDict={}
    for mydict in dicts:
        resDict=dict(resDict,**mydict)
    return resDict

if __name__ == "__main__":
    a={'a':'aa','b':'bb'}
    b={'c':'cc','d':'dd'}
    e={'e':'eeeee'}
    res = dictMerge(a,b,e)
    print res