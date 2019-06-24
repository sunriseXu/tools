#!/bin/sh

echo "uninstall app from smartphone"
echo "usage:unins.sh <packageName>"
packageName=$1
adb uninstall $packageName