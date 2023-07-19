set -x

${1}/wsk action delete ${2}

rm ${2}_function.code.py