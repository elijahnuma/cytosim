for j in ../job*
do echo Clearing $j && rm -r $j/save/Data_Files && for r in $j/save/*
do rm $r/*.dat
done
done
