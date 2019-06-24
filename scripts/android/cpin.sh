#!/bin/sh

echo original parameters=[$*]
echo original OPTIND=[$OPTIND]
echo "usage:cpin.sh <app_hash> <app_name>"
appHash=$1
appName=$2
echo appHash=$appHash
echo appName=$appName

source_dir=~/Desktop/malware/pay/
dest_dir=~/Desktop/malware/
source_file=$source_dir$appHash
dest_file=$dest_dir$appName
cp $source_file $dest_file
adb install $dest_file