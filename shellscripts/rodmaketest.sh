for m in 90000 100000
do for h in 2 4 6 8 16 32
do bash ../edit.sh "new [0-9]* solid" "new $m solid" ${h}heads.cym 
cp ${h}heads.cym .. && cd .. && bash maketest.sh *.cym 10 && cd ./motortemplates/ 
done 
done
