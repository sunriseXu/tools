from modules import FileUtils
from modules import CollectionUtils
from modules import RexUtils
import platform
import os


# dictPath = 'permissionFromApiDesc.json'
# permissionDPath = 'D:\\androidsdkdoc\\permission28.json'

# myDict = FileUtils.readDict(dictPath)
# permissionDict = FileUtils.readDict(permissionDPath)
# dangerousPer = permissionDict['dangerous']
# keys = sorted(myDict.keys())
# for key in keys:
#     if key not in dangerousPer:
#         continue
#     value = myDict[key]
#     classkeys = sorted(value.keys())

#     print(key)
#     for classkey in classkeys:
#         apis = value[classkey]
#         apis = [i.split('(')[0] for i in apis]
#         apis = sorted(list(set(apis)))
#         for api in apis:
#             print('\t'+classkey+'->'+api)

dirname = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk28\\jsonRes'
sensitiveApiList = FileUtils.readList('C:\\Users\\limin\\Desktop\\sensitive_api.txt')
resDir = 'C:\\Users\\limin\\Desktop\\sensApi'
FileUtils.mkdir(resDir)
notexist=[]
for item in sensitiveApiList:
    className = item.split('->')[0]
    apiName = item.split('->')[1]
    fileName = className+'.json'
    myPath = os.path.join(dirname,fileName)
    if not os.path.exists(myPath):
        print('%s not exists!' %className)
        notexist.append(className)
        continue
    jsonDict = FileUtils.readDict(myPath)
    print(myPath)
    functionDict = jsonDict['Functions']
    resDict = {}
    for key, value in functionDict.items():
        # print key
        if apiName in key:
            resDict[key] = value
            # raw_input(s)
    resfileName = className+'.'+apiName+'.json'
    resPath = os.path.join(resDir,resfileName)
    FileUtils.writeDict(resDict, resPath)
    # print resDict
    # raw_input()
FileUtils.writeList(notexist,'C:\\Users\\limin\\Desktop\\notExistClass.txt')
input()

pathList = FileUtils.listDir(dirname)
functionCount = []
for myPath in pathList:
    jsonDict = FileUtils.readDict(myPath)
    className = jsonDict['ClassName']
    functionDict = jsonDict['Functions']
    for key,value in functionDict.items():
        if value['Permissions']:
            fullName = key
            perms = value['Permissions']
