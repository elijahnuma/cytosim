for j in ../job*
do echo Removing $j && if [[ $i -lt 10 ]]
then rm -r $j
else rm -r $j
fi
done   

