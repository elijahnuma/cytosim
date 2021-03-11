for m in 30000 40000 50000 60000 70000 80000 90000 100000
do bash edit.sh "new [0-9]* solid" "new $m solid" && for i in {1..5}
do h=$((2**i)) && cp ./${h}headswithmotorvel.cym .. 
cd .. && bash maketest.sh *.cym && cd anchortemplates/ 
done 
done
