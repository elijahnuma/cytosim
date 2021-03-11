for d in ./*/
do submit_lsf_GIT.py mem=20GB queue=belmonte avx=1 $d/*[0-9][0-9][0-9][0-9].cym 
done


