job_num=0
for i in $(seq $1 $2)
do job_start=$job_num && job_end=$(($job_num + 4))
sed -i "s/analyzejobs.sh .* rod/analyzejobs.sh $i $job_start $job_end rod/g" submitanalyzejobs.csh
bsub < submitanalyzejobs.csh
job_num=$(($job_num + 5))
done
