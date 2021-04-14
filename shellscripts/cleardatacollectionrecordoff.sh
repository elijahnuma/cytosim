recordoff_num=$(($(ls recordoffs | wc -l) - 1))
for i in $(seq 0 $recordoff_num)
do echo Removing recordoff$i... && rm -r recordoffs/recordoff$i
done
rm -r recordoffs
