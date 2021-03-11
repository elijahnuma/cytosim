for m in 100 200 300 400 500 600 700 800 900 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000 20000 30000 40000 50000 60000 70000 80000 90000 100000
do bash edit.sh "new [0-9]* solid" "new $m solid" && for h in 2 4 6 8 16 32
do cp ./${h}headswithmotorvel.cym ../tests/ && cd ../tests/ 
bash ../maketest.sh *.cym 10 && cd ../anchortemplates/ 
done 
done
