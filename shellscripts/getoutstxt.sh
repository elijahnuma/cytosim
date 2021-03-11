job_num=$(($(ls ../.. | grep 'job' | wc -l)-1))
run_num=$(ls *.txt | wc -l)
for i in {0..9}
do echo Grabbing out $i && for o in {1..10}
do cp ../../job0$i/logs/out_${o}.txt ./out$run_num.txt && run_num=$(($run_num + 1))
done
done

for i in $(seq 10 $job_num)
do echo Grabbing out $i && for o in {1..10}
do cp ../../job$i/logs/out_${o}.txt ./out$run_num.txt && run_num=$(($run_num + 1))
done
done


