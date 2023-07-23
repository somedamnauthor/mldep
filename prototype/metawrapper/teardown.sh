sudo docker rm -f ${1} haproxy

wsk action delete ${1}
