analyze_num=$(($(ls -d analyzes[0-9]* | wc -l) + 1))
rj_num=0 # running job number
ft_num=$(ls tests | wc -l) # final test number
sim_num=$(ls tests/test_${ft_num} | wc -l)
job_num=$(ls -d ../../job* | wc -l)
st_num=$(($((ft_num - $(($job_num / $sim_num)))) + 1)) # start test number
mkdir analyzes$analyze_num
for i in $(seq $st_num $ft_num)
do mkdir analyzes$analyze_num/analyze$i && cd analyzes$analyze_num/analyze$i
job_start=$rj_num && job_end=$(($(($rj_num + $sim_num)) - 1))
cp ../../submitanalyzejobs.csh .
sed -i "s/analyzejobs.sh .* .*/analyzejobs.sh $i $job_start $job_end $1/g" submitanalyzejobs.csh
bsub < submitanalyzejobs.csh
rj_num=$(($rj_num + $sim_num))
cd ../../
done
