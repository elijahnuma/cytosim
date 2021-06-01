for c in ./checks$1/*
do job_success=$(grep 'FAILED:   0' $c/stdout* | wc -l)
if [[ $job_success -ne 1 ]]
then echo $c failed && grep 'FAILED' $c/stdout*
fi
done
