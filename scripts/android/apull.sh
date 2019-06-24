#!/bin/sh

echo "adb pull app file from smartphone"
echo "usage:apull.sh <packageName>"
packageName=$1
source_dir=/data/user/0/$packageName
dest_dir=~/Desktop/unshell
adb root
echo source_dir=$source_dir
echo dest_dir=$dest_dir
adb pull $source_dir $dest_dir