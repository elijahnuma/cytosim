for r in ./recordoffs/*
do echo Removing $r && rm -r $r
done
rm -r recordoffs
for c in ./checks*/*
do echo Removing $c && rm -r $c
done
rm -r checks*
