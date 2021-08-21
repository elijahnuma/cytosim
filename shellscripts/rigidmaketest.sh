for m in 90000 100000
do for h in 2 4 6 8 16 32
do rd=./rigidrods # rod directory 
bash ../edit.sh "new [0-9]* solid" "new $m solid" $rd/${h}headsrigid.cym 
cp $rd/${h}headsrigid.cym .. && cd .. && bash maketest.sh *.cym 10 && cd ./motortemplates/ 
done 
done
