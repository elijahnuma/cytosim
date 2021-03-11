job_num=$(($(ls .. | grep 'job' | wc -l)-1))
mkdir recordoffs
for i in $(seq 0 $job_num)
do mkdir recordoffs/recordoff$i && cd recordoffs/recordoff$i
cp ../../*.py . && sed -i -r "s/job_list\[[0-9]*\]/job_list[$i]/g" recordoff.py
bsub < ../../submitrecordoff.csh && cd ../..
done
