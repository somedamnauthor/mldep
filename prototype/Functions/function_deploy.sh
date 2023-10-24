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

number=$3
# Loop to run the wsk action create command 'number' times
for i in $(seq 1 $number); do
    action_name="${2}$i"
    # ${1}/wsk action create $action_name --docker somedamnauthor/custom_ml_runtime:mldepv5 ${2}_function_code.py --memory 1024 --web true
    wsk action create $action_name --docker somedamnauthor/custom_ml_runtime:mldepv5 ${2}_function_code.py --memory 1024 --web true
done

# ${1}/wsk action create ${2} --docker somedamnauthor/custom_ml_runtime:mldepv5 ${2}_function_code.py --memory 1024 --web true

set +x

echo "----------------------------------------------------"
echo "Function Wrapper: Creating API from action"
echo "----------------------------------------------------"

set -x

# output=$(${1}/wsk api create /predict post ${2})

# Loop to run the wsk api command 'number' times
for i in $(seq 1 $number); do
    action_name="${2}$i"
    # ${1}/wsk api create /$action_name /predict post $action_name
    wsk api create /$action_name /predict post $action_name
done

# set +x

# echo "----------------------------------------------------"
# echo "Function Wrapper: Acquiring API endpoint"
# echo "----------------------------------------------------"

# set -x

# regex='http://[^ >]+'

# result=$(echo "$output" | grep -Eo "$regex" | head -1)

# result=${result%/predict}

# result=$(echo "$result" | sed 's|http://||g')

#echo "  server ${2}_function1 $result check" >> ../loadbalancer/haproxy.cfg

#sudo docker kill -s HUP haproxy
