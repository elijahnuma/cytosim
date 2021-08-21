for m in 100 200 300 400 500 600 700 800 900 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000
do for h in 2 4 6 8 16 32
do rd=./flexiblerods/800nmsegmentation # rod directory
bash ../edit.sh "new [0-9]* fiber minifilament" "new $m fiber minifilament" $rd/${h}headsflexible.cym 
cp $rd/${h}headsflexible.cym .. && cd .. && bash maketest.sh *.cym 10 && cd ./motortemplates/ 
done 
done
