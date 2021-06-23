gd=$PWD # git directory
cd .. && cd /share/belmonte/egnuma
sd=$PWD # share directory
for d in $sd/cyms/ $sd/cyms/motortemplates/ $sd/datacollection/ $sd/datacollection/data/
do cp $d/*.sh $gd/shellscripts
cp $d/*.csh $gd/cshellscripts
cp $d/*.txt $gd/textfiles
cp $d/*.py $gd/pythonscripts
cp $d/*.cym $gd/cymheadtemplates
done
