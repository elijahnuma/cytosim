for c in ./checks[0-9]*/*
do echo Removing $c && rm -r $c
done
rm -r checks[0-9]*
for r in ./recordoffs[0-9]*/*
do echo Removing $r && rm -r $r
done
rm -r recordoffs[0-9]*
