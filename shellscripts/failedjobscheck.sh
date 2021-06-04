checks_num=$(($(ls -d checks[0-9]* | wc -l) + 1))
job_num=$(($(ls .. | grep 'job' | wc -l)-1))
mkdir checks$checks_num
for i in $(seq 0 $job_num)
do mkdir checks$checks_num/check$i && cd checks$checks_num/check$i
if [[ $i -ge 0 && $i -lt 10 ]]
then j=0$i
else j=$i
fi
cp ../../submitfailedjobscheck.csh . && sed -i -r "s/job[0-9]*/job$j/g" submitfailedjobscheck.csh
bsub < submitfailedjobscheck.csh && cd ../.. && echo $j
done
