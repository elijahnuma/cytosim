job_num=$(ls -d ../job* | wc -l)
recordoff_num=$(($(ls -d recordoffs[0-9]* | wc -l) + 1))
mkdir recordoffs$recordoff_num
for j in $(seq 0 $(($job_num - 1)))
do mkdir recordoffs$recordoff_num/recordoff$j 
if [[ $j -lt 10 ]]
then df=0$j
else df=$j
fi
cd .. && df=$PWD/job$df/save/Data_Files && cd datacollection/
cd recordoffs$recordoff_num/recordoff$j
cp ../../*.py . && sed -i -r "s/job_list\[[0-9]*\]/job_list[$j]/g" recordoff.py
if [[ ! -d $df ]]
then echo Recording job $j && bsub < ../../submitrecordoff.csh 
fi
cd ../..
done
