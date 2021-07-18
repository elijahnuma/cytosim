failed_jobs=()
for i in $(seq $1 $2)
do if [[ $i -lt 10 ]]
then j=0$i
else j=$i
fi
echo Job$j && ls ../job$j/save/Data_Files
output=$(ls ../job$j/save/Data_Files)
if ! [[ $output =~ 'Rdata.csv' ]]
then failed_jobs+=($i)
fi
done
echo ${failed_jobs[@]} > failedjobs.txt
