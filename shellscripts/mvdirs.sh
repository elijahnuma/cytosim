for d in ./test_*/
do for i in {1..5} 
do mv $d${i} $d$(($i-1))
done
done
