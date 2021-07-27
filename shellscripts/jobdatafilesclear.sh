for j in ../job*
do echo Clearing $j && rm -r $j/save/Data_Files && rm $j/save/run00*/*.dat
done
