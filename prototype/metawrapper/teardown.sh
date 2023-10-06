# Check if the YAML file exists
if [ ! -f "config.yaml" ]; then
    echo "Error: 'config.yaml' file not found."
    exit 1
fi

# Read the input parameters from the YAML file using Python and export them as environment variables
eval "$(python3 - <<END
import yaml

with open('config.yaml', 'r') as file:
    data = yaml.safe_load(file)

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

flattened_data = flatten_dict(data)

for key, value in flattened_data.items():
    print(f"export {key}='{value}'")
END
)"


if [ $lb_rootAccess = "true" ]; then
    lb_perm_string="sudo"
else
    lb_perm_string=""
fi

if [ $container_rootAccess = "true" ]; then
    container_perm_string="sudo"
else
    container_perm_string=""
fi


# TEARDOWN BEGINS

containers=$($lb_perm_string docker ps -a --format "{{.Names}}" | grep "^${1}")

# Loop through and remove each container
for container in $containers; do
    echo "Removing container: $container"
    $lb_perm_string docker rm -f "$container"
done

$lb_perm_string docker rm -f haproxy

# wsk action delete ${1}

# List all actions in your namespace
actions=$(wsk action list | awk '{print $1}')

# Loop through the action names and delete each one
for action in $actions; do
    wsk action delete "$action"
done

rm ../Functions/${1}_model_code.py

sh ../VM/remove_vm.sh
