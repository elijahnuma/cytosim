x=$PWD && cd ../../ && y=$PWD && cd $x && z=$x/tests/test_${1} 
sim_num=$(($(ls tests/test_${1} | wc -l)-1))
for i in $(seq $2 $3)
do if [[ $i -ge 0 && $i -lt 10 ]]
then echo Analyzing job0$i... && cd $y/job0$i/save/
else echo Analyzing job$i... && cd $y/job$i/save/
fi
mkdir $z/$i/ && cp -r ./Data_Files/ $z/$i/
mkdir $z/$i/reports/
for d in ./run****/
do cd $d && n=$(basename $d)
if [[ "$4" == "point" ]]
then reportGIT couple > ${n}report.txt 
elif [[ "$4" == "rod" ]]
then reportGIT single > ${n}report.txt
fi
cp ${n}report.txt $z/$i/reports && cd .. 
done
done

# if folders do not start with 0
if [[ $2 -ne 0 ]]
then for i in $(seq 0 $sim_num)
do w=$(($2+$i)) && mv $z/$w/Data_Files $z/$i/ && mv $z/$w/reports $z/$i && rm -r $z/$w
done
fi 

