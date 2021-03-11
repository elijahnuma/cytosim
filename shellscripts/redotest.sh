# change .cym file in 0/ dir 
test_number=$(($(ls | grep "test_[0-9]*" | wc -l)+1))
bash copytest.sh $1 "$2" "$3"
bash deletetest.sh $1 false
mv test_${test_number}/ test_${1}/
cd ../datacollection/data/
mv test_${test_number}/ test_${1}/
