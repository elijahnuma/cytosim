lc=0 # loop counter
failed_jobs=(`cat failedjobs.txt`)
fj_num=${#failed_jobs[@]}
finaltest_num=$(ls data/tests | wc -l)
sim_num=$(ls data/tests/test_${finaltest_num} | wc -l)
job_num=$(($(ls -d ../job* | wc -l) - $((fj_num * $sim_num))))
for fj in ${failed_jobs[@]}
do sjb_num=$(($fj - $(($fj % $sim_num)))) # starting job batch number
for n in $(seq 0 $(($sim_num - 1)))
do m=$(($sjb_num + $n)) && if [[ $m -ge 0 && $m -lt 10 ]]
then oldjobdir_num=0$m
else oldjobdir_num=$m
fi
m=$(($(($job_num + $n)) + $lc)) && if [[ $m -ge 0 && $m -lt 10 ]]
then newjobdir_num=0$m
else newjobdir_num=$m
fi
echo Deleting ../job$oldjobdir_num 
echo rm -r ../job$oldjobdir_num
echo mv ../job$newjobdir_num ../job$oldjobdir_num
done
lc=$(($lc + $sim_num))
done
