job_num=$(($(ls ../.. | grep 'job' | wc -l)-1))
msg_num=$(ls *.cmo | wc -l)
for job in $(seq 0 $job_num)
do if [[ $job -ge 0 && $job -lt 10 ]]
then j=0$job
else j=$job
fi
echo Grabbing messages from job $j && for r in ../../job$j/save/run*
do cp $r/messages.cmo ./messages$msg_num.cmo && msg_num=$(($msg_num + 1))
done
done

