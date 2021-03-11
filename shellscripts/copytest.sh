# always escape brackets and asterisks
file_name=$(basename $(find ./test_${1}/0* -type f -name "*[^0-9].cym")) # finds file name
cp $(find ./test_${1}/0* -type f -name "*[^0-9].cym") . # copies target folder into here
bash editconfigs.sh "$2" "$3" $file_name # desired alteration
bash maketest.sh $file_name
