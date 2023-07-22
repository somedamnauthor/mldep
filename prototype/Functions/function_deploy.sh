# sample usage: 
# sh function_deploy.sh /home/srishankar/openwhisk bert 

echo "----------------------------------------------------"
echo "Function Wrapper: Creating function code"
echo "----------------------------------------------------"

set -x

cat ../models/${2}/${2}_code.py main_method_code.py > ${2}_function_code.py

set +x

echo "----------------------------------------------------"
echo "Function Wrapper: Creating OpenWhisk action"
echo "----------------------------------------------------"

set -x

${1}/wsk action create ${2} --docker somedamnauthor/custom_ml_runtime:mldepv5 ${2}_function_code.py --memory 1024 --web true

set +x

echo "----------------------------------------------------"
echo "Function Wrapper: Creating API from action"
echo "----------------------------------------------------"

set -x

output=$(${1}/wsk api create /predict post ${2})

set +x

echo "----------------------------------------------------"
echo "Function Wrapper: Acquiring API endpoint"
echo "----------------------------------------------------"

regex='http://[^ >]+'

result=$(echo "$output" | grep -Eo "$regex" | head -1)

result=${result%/predict}

result=$(echo "$result" | sed 's|http://||g')

#echo "  server ${2}_function1 $result check" >> ../loadbalancer/haproxy.cfg

#sudo docker kill -s HUP haproxy