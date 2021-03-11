x=$PWD && cd ../../ && y=$PWD && cd $x
for i in $(seq $2 $3)
do if [[ $i -ge 0 && $i -lt 10 ]]
then echo Collecting job0$i... && cp -r $y/job0$i/save/Data_Files/ ./test_${1}/$i
else echo Collecting job$i... && cp -r $y/job$i/save/Data_Files/ ./test_${1}/$i
fi
done
