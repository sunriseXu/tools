#!/bin/sh

echo "adb pull file and find string in smali"
echo "apull.sh with fsmali.sh"
echo "usage: apfs.sh <packageName> <String>"
packageName=$1
souceDir=~/Desktop/unshell/$packageName
myString=$2
if [ ! -d $souceDir ];then
	~/Desktop/apull.sh $packageName
fi
echo "--------------pull finished---------------"
echo "--------------start find in samli--------"
echo souceDir=$souceDir
echo myString=$myString
~/Desktop/fsmali.sh -d $souceDir -f $myString
cd ~/Desktop