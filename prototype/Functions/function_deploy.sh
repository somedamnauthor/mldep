# sample usage: 
# sh function_deploy.sh /home/srishankar/openwhisk bert 

set -x

cat ../models/${2}/${2}_code.py main_method_code.py > ${2}_function_code.py

${1}/wsk action create ${2} --docker somedamnauthor/custom_ml_runtime:mldepv5 ${2}_function_code.py --memory 1024 --web true

${1}/wsk api create /predict post ${2}

# ${1}/wsk action invoke ${2} --result --param data "Give it to me, that thing, your [MASK] soul."

# # ${1}/wsk action invoke ${2} --result --param data ""