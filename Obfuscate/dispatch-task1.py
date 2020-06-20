#coding=utf-8
import argparse
import os
import sys
import random
import hashlib
import shutil
def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)
	return path
def readList(myPath):
	reslist=[]
	if not os.path.exists(myPath):
		temp=open(myPath,'w')
		temp.close()
	with open(myPath,"r") as file:
		reslist=file.readlines()
	reslist = [i.strip().strip('\r') for i in reslist]
	return reslist


def writeList(myList,myPath):
	with open(myPath,"w") as file:
		for item in myList:
			item=str(item).strip()+"\n"
			file.write(item)


if __name__ == "__main__":
    #maping文件的路径 和 学生id文件
    mapPath = sys.argv[1]
    stuIdPath = sys.argv[2]
    amount = 10
    mapList = readList(mapPath)

    mapList = [i.strip() for i in mapList]
    stuIdList = readList(stuIdPath)
    baseDir = 'lab6/'
    
    for stuId in stuIdList:
        print(stuId)
        stuDir = baseDir+stuId+"/task1"
        mkdir(stuDir)
        questionPath = stuDir + '/' +'task_question.txt'
        hashPath = stuDir + '/'+'task_md5.txt'
        anwserPath = stuDir + '/' + 'task_answer.txt'

        anwserMapList = list(random.sample(mapList, amount))
        
        questionList = [i.split()[0] for i in anwserMapList]
        answerList = [i.split()[1].strip() for i in anwserMapList]
        hashList = []
        for i in answerList:
            m = hashlib.md5()
            b = i.encode(encoding='utf-8')
            m.update(b)
            tmp = m.hexdigest()
            hashList.append(tmp)
        writeList(answerList, anwserPath)
        writeList(hashList, hashPath)
        writeList(questionList, questionPath)
        src = 'selfcheck.py'
        dest = stuDir+'/'+'selfcheck.py'
        shutil.copy(src,dest)

