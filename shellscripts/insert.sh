mv test_${1} insert_test
if [[ $1 -lt $2 ]]
then for i in $(seq $1 $(($2 - 1)))
do hole=$(($i + 1)) && mv test_${hole} test_${i}
done
else for i in $(seq $(($1 - 1)) -1 $2)
do hole=$(($i + 1)) && mv test_${i} test_${hole}
done
fi
mv insert_test test_${2}
