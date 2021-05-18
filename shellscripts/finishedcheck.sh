for c in ./checks$1/*
do job_success=$(grep 'FINISHED:  10' $c/stdout* | wc -l)
if [[ $job_success -ne 1 ]]
then echo $c failed && grep 'FINISHED' $c/stdout*
fi
done
