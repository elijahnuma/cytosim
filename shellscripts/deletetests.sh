for i in $(seq $1 $2)
do echo Deleting test $i && rm -r ./tests/test_${i}/ && rm -r ../datacollection/data/tests/test_${i}
done
