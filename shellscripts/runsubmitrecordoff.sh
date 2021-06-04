recordoff_num=$(($(ls -d recordoffs[0-9]* | wc -l) + 1))
mkdir recordoffs$recordoff_num
for i in $(seq $1 $2)
do mkdir recordoffs$recordoff_num/recordoff$i && cd recordoffs$recordoff_num/recordoff$i
cp ../../*.py . && sed -i -r "s/job_list\[[0-9]*\]/job_list[$i]/g" recordoff.py
bsub < ../../submitrecordoff.csh && cd ../..
done
