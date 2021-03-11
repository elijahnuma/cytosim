for f in ./*.cym
do sed -i "s/${1}/${2}/g" $f
done
