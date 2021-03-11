for d in ./*/
do rm -f $d/*[0-9][0-9][0-9][0-9].cym && pre_config_JMB.py $d/ $d/*[^0-9].cym
done



