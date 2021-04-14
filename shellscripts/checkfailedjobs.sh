job_num=$(($(ls .. | grep 'job' | wc -l)-1))
mkdir checks
for i in $(seq 0 $job_num)
do mkdir checks/check$i && cd checks/check$i
sed -i -r "s/job_list\[[0-9]*\]/job_list[$i]/g" recordoff.py
bsub < ../../submitcheckfailedjobs.csh && cd ../..
done
