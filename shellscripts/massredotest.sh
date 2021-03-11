for i in {68..91}
do bash redotest.sh $i "nb_steps = 1000" "nb_steps = 200"
done
bkill 0 
rm -r ../job*
for i in {68..91}
do bash redotest.sh $i "R = \[0.1+0.1\*i for i in range(10)\]" "R = sorted(list(set(\[round(i\*10\*\*-j,3) for i in$bjobs
done
bjobs
