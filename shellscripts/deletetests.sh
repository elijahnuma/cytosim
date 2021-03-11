for i in $(seq $1 $2)
do echo Deleting test $i && rm -r ./test_${i}/ && rm -r ../datacollection/data/test_${i}
done
