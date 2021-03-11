for i in $(seq 0 $(($(ls recordoffs | wc -l) - 1)))
do echo Removing recordoff$i... && rm -r recordoffs/recordoff$i
done
rm -r recordoffs
