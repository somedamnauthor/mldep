# sample usage: 
# sh function_deploy.sh /home/srishankar/openwhisk bert 

set -x

cat ../models/${2}/${2}_code.py main_method_code.py > ${2}_function_code.py

${1}/wsk action create ${2} --docker somedamnauthor/custom_ml_runtime:mldepv5 ${2}_function_code.py --memory 1024 --web true

output=$(${1}/wsk api create /predict post ${2})

regex='http://[^ >]+'

result=$(echo "$output" | grep -Eo "$regex" | head -1)

result=${result%/predict}

result=$(echo "$result" | sed 's|http://||g')

#echo "  server ${2}_function1 $result check" >> ../loadbalancer/haproxy.cfg

#sudo docker kill -s HUP haproxy
