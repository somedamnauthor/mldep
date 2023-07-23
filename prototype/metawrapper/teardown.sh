sudo docker rm -f ${1} haproxy

wsk action delete ${1}

rm ../Functions/${1}_model_code.py