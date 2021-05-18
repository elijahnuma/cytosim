for c in ./checks[0-9]*/*
do echo Removing $c && rm -r $c
done
rm -r checks[0-9]*
