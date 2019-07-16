from modules import FileUtils
from modules import CollectionUtils
from modules import RexUtils
import platform



if __name__ == "__main__":
    rogdir='/home/limin/Desktop/malware/rog'
    roglist = FileUtils.listDir2(rogdir)
    roglist = [str(i) for i in roglist]

    tmpxxpath='./tmpxx'
    tmplist = FileUtils.readList(tmpxxpath)
    
    idx = 0
    end = len(tmplist)/4
    findlist = []
    showlist = []
    for idx in range(0,end):
        hashidx = idx*4
        apkhash = str(tmplist[hashidx])
        elfname = tmplist[hashidx+1].strip()
        smaliname = tmplist[hashidx+3].strip()
      
        elflen = len(elfname.split(':'))
        smalilen = len(smaliname.split())
       
        if elflen>1 and smalilen>1 and (apkhash in roglist):
            findlist.append(apkhash)
            showlist.append(apkhash)
            showlist.append(tmplist[hashidx+1])
            showlist.append(tmplist[hashidx+3])
    findlistpath='/home/limin/Desktop/find.txt'
    showlistpath='/home/limin/Desktop/show.txt'
    FileUtils.writeList(findlist,findlistpath)
    FileUtils.writeList(showlist,showlistpath)

    destdir = '/home/limin/Desktop/rogwithelf'
    FileUtils.listCopy(findlist,rogdir,destdir)



    
    