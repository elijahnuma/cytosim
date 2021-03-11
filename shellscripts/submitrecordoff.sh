for i in $(seq $1 $2)
do sed -i -r "s/job_list\[[0-9]*\]/job_list[$i]/g" recordoff.py && bsub < run_mycode.csh && sleep $3
done
bjobs
