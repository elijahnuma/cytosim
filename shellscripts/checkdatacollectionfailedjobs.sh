sim_num=$(ls ../job00/save/ | wc -l)
job_num=$(($(ls .. | grep 'job' | wc -l)-1))
for j in ../job*
do job_success=$(CheckSims.py $j | grep 'FINISHED:  10' | wc -l)
if [[ $job_success -ne 1 ]]
then for r in $j/save/*
do run_success=$(du $r/properties.cmo | cut -f1)
if [[ $run_success -ne 1 ]]
then echo $r has no properties.cmo file
fi
done
fi
done
