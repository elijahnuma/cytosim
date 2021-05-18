for r in ./recordoffs[0-9]*/*
do echo Removing $r && rm -r $r
done
rm -r recordoffs[0-9]*
