rm -r ./test_${1}/
cd ..
if $2
then rm -r job*
fi
cd datacollection/data && rm -r ./test_${1}/
