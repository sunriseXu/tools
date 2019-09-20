from modules import FileUtils
from modules import CollectionUtils
from modules import RexUtils
import platform
import os
import re

def rexFind(rex,content):
    '''
    simplely find all string which matches rex in content, return list
    
    '''
    pattern=re.compile(rex,re.S)
    resList=re.findall(pattern,content)
    return resList
destDir = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk28\\jsonRes'

jsonPaths = FileUtils.listDir(destDir)
# resPath = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\seeAlso.json'
seeAlsoResDict = {}
for p in jsonPaths:
    mydict = FileUtils.readDict(p)
    className = mydict['ClassName']
    funcDict = mydict['Functions']
    # seeAlsoResDict[className] = {}
    flag = False
    for key in funcDict:
        funcBody = funcDict[key]
        descript = funcBody['Description']

        # reg = r'\[(.*?)\]\((.*?)\)'
        # res = rexFind(reg,descript)
        
        seeAlso = funcBody['SeeAlso']
        if len(seeAlso)>0:
            final = []
            tmp = []
            for aa in res:
                if aa[0] in tmp:
                    continue
                aa = [aa[0],aa[1]+')']
                final.append(aa)
                tmp.append(aa[0])
            flag = True
            seeAlsoResDict[className][key] = final
            # print seeAlsoResDict
            # input()
    if not flag:
        seeAlsoResDict.pop(className)
FileUtils.writeDict(seeAlsoResDict,resPath)