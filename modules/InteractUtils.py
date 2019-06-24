import sys
import re

def showList(myList):
    '''
    show list with index
    '''
    idx=0
    for i in myList:
        print("%d: %s" %(idx,i))
        idx+=1
    return idx

def selectListItemByIdx(myList):
    '''
    this function is not safe, it is possible to occur indexerror
    '''
    print("plese choose item in List:")
    idx=sys.stdin.readline().strip()
    while not idx.isdigit():
        print("again,please input number:")
        idx=sys.stdin.readline().strip()
    selectedItem=myList[int(idx)]
    return selectedItem

def contDigit(myStr):
	pattern = re.compile('[0-9]+')
	match = pattern.findall(myStr)
	if match:
		return True
	else:
		return False