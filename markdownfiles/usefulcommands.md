for loop with input:
for i in $(seq $1 $2)

addition:
sum=$(($addend_1 + $addend_2))

disk usage in curent folder:
du -hs

check target text count
$(fulltext.txt | grep "target text" | wc -l)

check if jobs successfully ran
CheckSims.py ../job* | grep 'FINISHED:  10' | wc -l

check if jobs successfully analyzed
bash checkjobs.sh | grep 'Rdata.csv' | wc -l

run FiberPoints.dat manually while in job folder
scan.py "reportGIT fiber:points > FiberPoints.dat" run* 

git ssh
git@github.com:elijahnuma/cytosim.git

