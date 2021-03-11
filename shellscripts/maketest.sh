test_number=$(($(ls | grep "test_[0-9]*" | wc -l)+1))
test_dir=test_${test_number}
mkdir ./$test_dir/ && mkdir ./$test_dir/0/ && mv $1 ./$test_dir/0/ 
bash editconfigs.sh " " " " ./$test_dir/0/${1}
cd ./$test_dir/ && bash ../preconfigs.sh && bash ../copysims.sh 5 && bash ../runjobs.sh 
cd .. && x=$PWD && cd ../datacollection/data/
mkdir ./$test_dir && mkdir ./$test_dir/0/
cd ./$test_dir/ && bash $x/copysims.sh 5
