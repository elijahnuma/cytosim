job_num=$(($(ls .. | grep 'job' | wc -l)-1))
mkdir checks$1
for i in $(seq 0 $job_num)
do mkdir checks$1/check$i && cd checks$1/check$i
if [[ $i -ge 0 && $i -lt 10 ]]
then j=0$i
else j=$i
fi
cp ../../submitcheckfailedjobs.csh . && sed -i -r "s/job[0-9]*/job$j/g" submitcheckfailedjobs.csh
bsub < submitcheckfailedjobs.csh && cd ../.. && echo $j
done
