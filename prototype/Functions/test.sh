output='ok: created API /predict POST for action /_/bert http://172.17.0.1:3234/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/predict'

regex='http://[^ >]+'

result=$(echo "$output" | grep -Eo "$regex" | head -1)

echo $result

result=${result%/predict}

result=$(echo "$result" | sed 's|http://||g')

echo $result
