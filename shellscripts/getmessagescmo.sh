job_num=$(($(ls ../.. | grep 'job' | wc -l)-1))
run_num=$(ls *.cmo | wc -l)
for i in {0..9}
do echo Grabbing job $i && for r in ../../job0$i/save/run*
do cp $r/messages.cmo ./messages$run_num.cmo && run_num=$(($run_num + 1))
done
done

for i in $(seq 10 $job_num)
do echo Grabbing job $i && for r in ../../job$i/save/run*
do cp $r/messages.cmo ./messages$run_num.cmo && run_num=$(($run_num + 1))
done
done   

