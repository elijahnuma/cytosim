job_num=$(($(ls .. | grep 'job' | wc -l)-1))
for i in $(seq 0 $job_num)
do total_successes=0 && for c in $i 
do job_success=$(grep 'FINISHED:  10' checks/check$c/stdout* | wc -l)
if [[ $job_success -eq 1 ]] 
then total_successes=$(($total_successes+1))
fi
done
if [[ $total_successes -lt 3 ]]
then echo Test $i failed && echo Successful jobs: $total_successes
fi
done
