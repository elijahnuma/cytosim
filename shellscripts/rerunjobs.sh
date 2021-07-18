for fj in `cat failedjobs.txt`
do finaltest_num=$(ls data/tests | wc -l)
sim_num=$(ls data/tests/test_${finaltest_num} | wc -l)
job_num=$(ls -d ../job* | wc -l)
i=$(($finaltest_num + 1)) && j=$(($job_num / $sim_num)) && k=$(($fj / $sim_num))
rerun_test=$(($(($i - $j)) + $k))
cd ../cyms/ && cp tests/test_${rerun_test}/0/*[^0-9].cym .
bash maketest.sh *.cym $sim_num
bash deletetests.sh $((finaltest_num + 1)) $((finaltest_num + 1))
cd ../datacollection
done
