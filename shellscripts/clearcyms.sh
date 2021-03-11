job_num=$(($(ls .. | grep 'job' | wc -l)-1))
cd ..
for i in $(seq 0 $job_num)
do echo Deleting job $i && if [[ $i -lt 10 ]]
then rm -r job0$i
else rm -r job$i
fi
done   
echo TEST LINE
