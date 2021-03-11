meta_num=$(($(ls -d data/metadata/messages_* | wc -l)+1))
mkdir messages_${meta_num}
mkdir outs_${meta_num}
cd messages* && bash ../data/metadata/getmessagescmo.sh && cd ..
cd outs* && bash ../data/metadata/getoutstxt.sh
