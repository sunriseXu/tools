#coding=utf-8
import xlwt
from xlwt import Workbook
def myCombinations(pNum):
    from itertools import combinations,permutations
    resList = []
    #计算每组人数
    perGroup = (int)(pNum / 3)
    pSet = set(range(1,pNum+1))
    #取出第一组的情况
    for grpA in combinations(pSet, perGroup):
        #计算剩余两组的差集
        grpBC = pSet.difference(grpA)
        #取出第二组的情况
        for grpB in combinations(grpBC, perGroup):
            #计算第三组的情况
            grpC = tuple(grpBC.difference(grpB))
            resList.append([grpA, grpB, grpC])
    return resList

def genExcel(data, excelPath):
    w = Workbook()
    ws = w.add_sheet('1')
    for i in range(1, 7):
        ws.write(0, i,'{}'.format(i))
    for i in range(0, len(data)):
        row = data[i]
        rowNum = i + 1
        ws.write(rowNum, 0, rowNum)
        gA, gB, gC = tuple(row)
        for item in gA:
            ws.write(rowNum, item, "A")
        for item in gB:
            ws.write(rowNum, item, "B")
        for item in gC:
            ws.write(rowNum, item, "C")
    w.save(excelPath)

if __name__ == "__main__":
    
    result =  myCombinations(6)
    excelPath = './result.xls'
    genExcel(result, excelPath)