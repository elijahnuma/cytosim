job_num=$(($(ls .. | grep 'job' | wc -l)-1))
for i in $(seq 0 $job_num)
do if [[ $i -ge 0 && $i -lt 10 ]]
then echo Job0$i... && ls ../job0$i/save/Data_Files
else echo Job$i... && ls ../job$i/save/Data_Files
fi
done
