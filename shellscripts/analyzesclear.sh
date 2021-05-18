for a in ./analyzes/*
do echo Removing $a && rm -r $a
done
rm -r analyzes
