test_number=$(($(ls | grep "test_[0-9]*" | wc -l)+1))
test_dir=test_${test_number}
mkdir ./$test_dir/ && mkdir ./$test_dir/0/ && mv $1 ./$test_dir/0/ 
bash ../editconfigs.sh " " " " ./$test_dir/0/${1} && sim_num=$2
cd ./$test_dir/ && bash ../../preconfigs.sh && bash ../../copysims.sh $sim_num && bash ../../runjobs.sh 
cd ../../ && x=$PWD && cd ../datacollection/data/
mkdir ./tests/$test_dir && mkdir ./tests/$test_dir/0/
cd ./tests/$test_dir/ && bash $x/copysims.sh $sim_num
