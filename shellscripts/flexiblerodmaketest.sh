for m in 50000 60000 70000 80000
do for h in 2 4 6 8 16 32
do bash ../edit.sh "new [0-9]* fiber minifilament" "new $m fiber minifilament" ${h}headsflexible.cym 
cp ${h}headsflexible.cym .. && cd .. && bash maketest.sh *.cym 10 && cd ./motortemplates/ 
done 
done
