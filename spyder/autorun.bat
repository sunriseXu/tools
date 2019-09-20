set var=13
rem ************循环开始了
:continue
set /a var+=1
echo 第%var%次循环
python androidSDKSpy.py -e %var%

if %var% lss 27 goto continue
rem ************循环结束了
echo 循环执行完毕
pause