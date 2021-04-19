for i in $(seq $1 $2)
do sim_num=$(($(ls tests/test_${1} | wc -l) - 1)) && echo Clearing test $i 
rm -r tests/test_${i}/* && for j in $(seq 0 $sim_num)
do mkdir tests/test_${i}/$j
done
done
