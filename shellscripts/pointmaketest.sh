for m in 70000 80000 90000 100000
do bash ../edit.sh "new [0-9]* myosin" "new $m myosin" stallforce.cym && for f in 4
do bash ../edit.sh "stall_force = [0-9]*" "stall_force = $f" stallforce.cym && cp stallforce.cym .. && cd .. 
bash maketest.sh *.cym 10 && cd  ./motortemplates/ 
done 
done
