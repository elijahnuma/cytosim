for i in $(seq $1 $2)
do if [[ $i -ge 0 && $i -lt 10 ]]
then echo Job0$i... && ls ../job0$i/save/Data_Files
else echo Job$i... && ls ../job$i/save/Data_Files
fi
done
