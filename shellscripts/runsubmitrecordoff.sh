mkdir recordoffs$1
for i in $(seq $2 $3)
do mkdir recordoffs$1/recordoff$i && cd recordoffs$1/recordoff$i
cp ../../*.py . && sed -i -r "s/job_list\[[0-9]*\]/job_list[$i]/g" recordoff.py
bsub < ../../submitrecordoff.csh && cd ../..
done
