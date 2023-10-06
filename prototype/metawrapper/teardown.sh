containers=$(sudo docker ps -a --format "{{.Names}}" | grep "^${1}")

# Loop through and remove each container
for container in $containers; do
    echo "Removing container: $container"
    sudo docker rm -f "$container"
done

sudo docker rm -f haproxy

# wsk action delete ${1}

# List all actions in your namespace
actions=$(wsk action list | awk '{print $1}')

# Loop through the action names and delete each one
for action in $actions; do
    wsk action delete "$action"
done

rm ../Functions/${1}_model_code.py

sh ../VM/remove_vm.sh