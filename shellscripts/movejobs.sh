finaltest_num=$(ls data/tests | wc -l)
sim_num=$(ls data/tests/test_${finaltest_num} | wc -l)
job_num=$(($(ls -d ../job* | wc -l) - $sim_num))
i=$(($finaltest_num + 1)) && j=$(($job_num / $sim_num)) && k=$(($1 / $sim_num))
rerun_test=$(($(($i - $j)) + $k))
startingjobbatch_num=$(($1 - $(($1 % $sim_num))))
for n in $(seq 0 $(($sim_num - 1)))
do m=$(($startingjobbatch_num + $n)) && if [[ $m -ge 0 && $i -lt 10 ]]
then oldjobdir_num=0$m
else oldjobdir_num=$m
fi
m=$(($job_num + $n)) && if [[ $m -ge 0 && $i -lt 10 ]]
then newjobdir_num=0$m
else newjobdir_num=$m
fi
echo Deleting ../job$oldjobdir_num && rm -r ../job$oldjobdir_num
mv ../job$newjobdir_num ../job$oldjobdir_num
done
