for i in {125..213}
do for j in {0..4}
do echo test $i, folder $j: && ls test_${i}/$j/Data_Files/
done
done
