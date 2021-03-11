sim_num=$(($(ls tests/test_${1} | wc -l) - 1))
for t in $(seq $1 $2)
do for s in $(seq 0 $sim_num)
do echo Checking test $t sim $s 
ls tests/test_${t}/$s/
done
done
