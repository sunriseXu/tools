#coding=utf-8
import argparse
from MatchUtils import StrOp
from MatchUtils import QueryOp
from MatchUtils import CreationOp
from MatchUtils import AlgorOp
from modules import InteractUtils
from modules import FileUtils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="find dex!!")
    parser.add_argument('-b', '--basePath', nargs='?',default="") #多个参数 默认放入list中 +表示至少一个 + 就放在list中
    parser.add_argument('-d', '--tarPath', nargs='?',default="")
    parser.add_argument('-c', '--cached', help='tmp dir', nargs='?',default="")
    parser.add_argument('-o', '--resname', help='get all class dict', nargs='?',default="")
    args = parser.parse_args() 
    basePath=args.basePath
    tarPath=args.tarPath
    cachedPath = args.cached
    output = args.resname
    basePackageDict = FileUtils.readDict(basePath)
    targetPackageDict = FileUtils.readDict(tarPath)
    baseClazz = 'com.linecorp.line.media.picker.fragment.sticker.b'
    resList = AlgorOp.calClazzConstStrSimilarity(basePackageDict,baseClazz,targetPackageDict,30)
    InteractUtils.showList(resList)
    