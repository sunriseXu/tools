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

def selectListItemByIdx(myList, prompt="plese choose item in List:"):
    '''
    this function is not safe, it is possible to occur indexerror
    '''
    print(prompt)
    idx=sys.stdin.readline().strip()
    while not idx.isdigit():
        print("again,please input number:")
        idx=sys.stdin.readline().strip()
    selectedItem=myList[int(idx)]
    return selectedItem

def getDigit(prompt="plese choose amount:"):
    '''
    this function is not safe, it is possible to occur indexerror
    '''
    print(prompt)
    amount=sys.stdin.readline().strip()
    while not amount.isdigit():
        print("again,please input number:")
        amount=sys.stdin.readline().strip()
    return int(amount)

def contDigit(myStr):
	pattern = re.compile('[0-9]+')
	match = pattern.findall(myStr)
	if match:
		return True
	else:
		return False