job_num=$(($(ls .. | grep 'job' | wc -l)-1))
mkdir recordoffs$1
for i in $(seq 0 $job_num)
do mkdir recordoffs$1/recordoff$i && cd recordoffs$1/recordoff$i
cp ../../*.py . && sed -i -r "s/job_list\[[0-9]*\]/job_list[$i]/g" recordoff.py
bsub < ../../submitrecordoff.csh && cd ../..
done
