mkdir analyzes
job_num=0
sim_num=$(($(ls tests/test_${1} | wc -l)-1))
for i in $(seq $1 $2)
mkdir analyzes/analyze$i && cd analyzes/analyze$i
do job_start=$job_num && job_end=$(($job_num + $sim_num))
cp ../../submitanalyzejobs.csh .
sed -i "s/analyzejobs.sh .* .*/analyzejobs.sh $i $job_start $job_end $3/g" submitanalyzejobs.csh
bsub < submitanalyzejobs.csh
job_num=$(($job_num + $(($sim_num + 1))))
cd ../../
done
