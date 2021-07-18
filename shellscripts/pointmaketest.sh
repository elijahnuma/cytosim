for m in 2000 3000 4000 5000 6000 
do bash ../edit.sh "new [0-9]* myosin" "new $m myosin" stallforce.cym && for f in 4
do bash ../edit.sh "stall_force = [0-9]*" "stall_force = $f" stallforce.cym && cp stallforce.cym .. && cd .. 
bash maketest.sh *.cym 10 && cd  ./motortemplates/ 
done 
done
