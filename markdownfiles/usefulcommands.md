for loop with input:
for i in $(seq $1 $2)

addition:
sum=$(($addend_1 + $addend_2))

disk usgae in current folder:
du -hs

check target text count:
$(fulltext.txt | grep "target text" | wc -l

check if jobs successfully ran:
CheckSims.py ../job* | grep 'FINISHED:  10' | wc -l

check if jobs successfully analyzed:
bash checkdatacollectiondatafiles.sh | grep 'Rdata.csv | wc -l

run FiberPoints.dat manually while in job folder:
scan.py "reportGIT fiber:points > FiberPoints.dat" run*

find rootdir -type f -delete
delete all files within subdirectories

find rootdir -name "*.ext" -type f -delete
delete all files with specific extension in subdirectories

/usr/local/usrapps/belmonte/bin/
file location for global python files

git url:
git clone https://github.com/elijahnuma/cytosim.git
