for m in 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000 20000 30000 40000 50000 60000
do bash ../edit.sh "new [0-9]* myosin" "new $m myosin" stopforce.cym && for f in 2 4 6 8 16 32
do bash ../edit.sh "stall_force = [0-9]*" "stall_force = $f" stopforce.cym && cp stopforce.cym .. && cd .. 
bash maketest.sh *.cym 10 && cd  ./motortemplates/ 
done 
done