test_number=$(($(ls ./tests/ | grep "test_[0-9]*" | wc -l)+1))
t=./tests/test_${test_number}
mkdir $t && mkdir $t/0/ && mv $1 $t/0/ 
bash editconfigs.sh " " " " $t/0/${1} && sim_num=$2
cd $t && bash ../../preconfigs.sh && bash ../../copysims.sh $sim_num && bash ../../runjobs.sh 
cd ../../ && x=$PWD && cd ../datacollection/data/
mkdir $t && mkdir $t/0/
cd $t && bash $x/copysims.sh $sim_num
