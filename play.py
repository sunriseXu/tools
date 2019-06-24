from modules.FileUtils import *

logDir='C:/Users/limin/Desktop/imageLogs/xxx/logs'
logsPath=listDir(logDir)
selectedList=[]
count=0
notfound=0
timeout=0
delegateCount=0
runtime=0
coredump=0
others=0
destDir='C:/Users/limin/Desktop/tmpAsan'
for item in logsPath:
    buf = readFile(item)
    if 'Sanitizer' in buf:
        count+=1
        # if 'leak' not in buf:
        selectedList.append(os.path.basename(item))
        continue
    if 'not found' in buf:
        notfound+=1
        continue
    if 'TIME' in buf:
        timeout+=1
        continue
    if 'runtime error' in buf:
        selectedList.append(os.path.basename(item))
        runtime +=1
        continue
    if 'core dump' in buf:
        selectedList.append(os.path.basename(item))
        coredump+=1
        continue
    
    others+=1
    print item

    


print count
print notfound
print timeout
print runtime
print coredump
# print delegateCount
print others

#         continue
#     if 'memory leaks' in buf:
#         continue
#     selectedList.append(os.path.basename(item))
# destDir='C:/Users/limin/Desktop/tmpAsan'
listCopy(selectedList,logDir,destDir)
