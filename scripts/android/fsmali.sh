#!/bin/bash

function getdir(){
	for element in `ls $1`
	do  
		dir_or_file=$1"/"$element
		if [ -d $dir_or_file ]
		then 
			getdir $dir_or_file
		else
			echo $dir_or_file
		fi  
	done
}
function getMethod(){
	arr=$1
	cut_prefix=$2
	prefix_len=${#cut_prefix}
	((prefix_len++))
	newarr=()
	for element in ${arr[*]}
	do
		result=$(echo $element | grep ".smali:")
		if [[ "$result" != "" ]]
		then
			subString=${element:prefix_len}
			subString2=${subString%%.*}
			subString3=${subString2////.}
		#echo $subString3
		if echo "${newarr[*]}" | grep -w "$subString3" &>/dev/null; then
			:
		else
			newarr[${#newarr[*]}]=$subString3
		fi
		#newarr[${#newarr[*]}]=$subString3
	fi 
done
echo ${newarr[*]}
}
echo original parameters=[$*]
echo original OPTIND=[$OPTIND]
while getopts ":d:f:" opt
do
	case $opt in
		d)
		echo "this is -d option. OPTARG=[$OPTARG] OPTIND=[$OPTIND]"
		source_dir=$OPTARG
		;;
		f)
		echo "this is -f option. OPTARG=[$OPTARG] OPTIND=[$OPTIND]"
		function_api=$OPTARG	
		;;
		?)
		echo "there is unrecognized parameter."
		exit 1
		;;
esac
done
#通过shift $(($OPTIND - 1))的处理，$*中就只保留了除去选项内容的参数，
#可以在后面的shell程序中进行处理
echo source_dir=$source_dir
echo function_api=$function_api
shift $(($OPTIND - 1))

echo remaining parameters=[$*]
#index=0
myarr=()
files=$(cd $source_dir && ls|sed "s:^:`pwd`/: ")
for file in $files; do
	#echo $file
	temp_file=`basename $file`
	result=$(echo $temp_file | grep "\.dex")
	if [[ "$result" != "" ]]       
	then
		echo $temp_file
		pdir=$(dirname "$file")
		output_dir=$pdir"/"${temp_file%.*}"-out"
	#echo $output_dir
	myarr[${#myarr[*]}]=$output_dir
	d2j-baksmali.sh -o $output_dir $file >/dev/null 2>&1
	#index=index+1	
fi
done
function showArray(){
	arr=$1
	for ele in ${arr[*]}
	do 
		echo $ele
	done
}
myMethods=()
for out_dir in ${myarr[@]}
do
	if [ ! -d $out_dir ];then
		echo ${out_dir}" not exist! d2j this dex failed! you had better check out manually!"
	else
	#echo "******"
	#echo $out_dir
	res=`find $out_dir -type f -name '*.smali'|xargs grep -i "$function_api"`
	if [[ "$res" != "" ]]
	then
		echo $out_dir
		ele_res=($(getMethod "${res[*]}" $out_dir))
		showArray "${ele_res[*]}"
		myMethods=(${myMethods[*]} ${ele_res[*]})
		#showArray "${myPackages[*]}"    
	fi
fi 
done
echo "***********total****************" 
showArray "${myMethods[*]}"

