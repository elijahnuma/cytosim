for m in 90000 100000
do bash edit.sh "new [0-9]* solid" "new $m solid" && for h in 2 4 6 8 16 32
do cp ./${h}headswithmotorvel.cym ../tests/ && cd ../tests/ 
bash ../maketest.sh *.cym 10 && cd ../anchortemplates/ 
done 
done
