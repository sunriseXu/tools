
import argparse
from rooms import FileRoom
from modules import FileUtils
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument('-c', '--dict', help='app name', nargs='?', default="")
    args = parser.parse_args()
    elfDict=args.dict
    dir3 = 'res/elfDictNor.txt'
    dictNor = FileUtils.readDict(dir3)
    norElfList = dictNor.values()
    norList = []
    for i in norElfList:
        for j in i:
            if j not in norList:
                norList.append(j)

    mydict = FileUtils.readDict(elfDict)
    resdict = FileRoom.statisticLists(mydict)
    for i in sorted(resdict.items(),key=lambda item: item[1][0]):
        if i[0] in norList:
            continue
        print i[0],i[1][0]
    
    dir1='res/elfDict.txt'
    dir2='res/smaliDict.txt'
    
    dict1=FileUtils.readDict(dir1)
    dict2=FileUtils.readDict(dir2)
    
    # print norList
    
    dict3={}
    for key,value in dict1.items():
        if len(value)>0 and (key in dict2.keys()) and len(dict2[key])>0:

            print key
            print('\telf:'),
            for i in value:
                if i not in norList:
                    print(i),
            print '\n'
            print '\tsmali',dict2[key]
    # print dict3