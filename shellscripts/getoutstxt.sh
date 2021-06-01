job_num=$(($(ls ../.. | grep 'job' | wc -l)-1))
out_num=$(ls *.txt | wc -l)
run_num=$(ls -d ../../job00/save/run* | wc -l)
for job in $(seq 0 $job_num)
do if [[ $job -ge 0 && $job -lt 10 ]]
then j=0$job
else j=$job
fi
echo Grabbing outs from job $j && for o in $(seq 1 $run_num)
do cp ../../job$j/logs/out_${o}.txt ./out$out_num.txt && out_num=$(($out_num + 1))
done
done
