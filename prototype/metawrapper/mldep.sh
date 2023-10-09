# Sample usage: sh mldep.sh

echo "----------------------------------------------------"
echo "MLDep: Reading input and setting variables"
echo "----------------------------------------------------"

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

# # Source the temporary file to set the environment variables
# source temp_env_vars.txt

# # Remove the temporary file
# rm temp_env_vars.txt

# Example: Using the variables in the rest of the script
echo "Model: $model"
echo "Function Weight: $function_weight"
echo "Function Deploy: $function_deploy"
echo "Function Instances: $function_instances"
echo "OpenWhisk Path: $function_openwhiskPath"
echo "Container Weight: $container_weight"
echo "Container Deploy: $container_deploy"
echo "Container Instances: $container_instances"
echo "Container Root Access: $container_rootAccess"
echo "VM Weight: $vm_weight"
echo "VM Deploy: $vm_deploy"
echo "VM Instances: $vm_instances"
echo "VM Libvirt Root Access: $vm_rootAccess"
echo "VM Cloud Image Directory: $vm_cloudImgDir"
echo "Load Balancer Root Access: $lb_rootAccess"

if [ $lb_rootAccess = "true" ]; then
    lb_perm_string="sudo"
else
    lb_perm_string=""
fi

echo "----------------------------------------------------"
echo "MLDep: Starting HAProxy with initial config"
echo "----------------------------------------------------"


set -x

cd ../loadbalancer

sh deploy_lb.sh $lb_rootAccess

set +x


echo "----------------------------------------------------"
echo "MLDep: Checking for Container Deployment"
echo "----------------------------------------------------"

if [ "$container_deploy" = "true" ]; then
  cd ../Container/lightweight/
  sh container_wrapper.sh $model $container_instances $container_rootAccess
  cd ..
fi

echo "----------------------------------------------------"
echo "MLDep: Checking for VM Deployment"
echo "----------------------------------------------------"

if [ "$vm_deploy" = "true" ]; then
  cd ../VM
  python3 vm_wrapper.py $model $vm_instances $vm_rootAccess $vm_cloudImgDir
fi

echo "----------------------------------------------------"
echo "MLDep: Checking for Function Deployment"
echo "----------------------------------------------------"

if [ "$function_deploy" = "true" ]; then
  cd ../Functions
  sh function_deploy.sh $function_openwhiskPath $model $function_instances
fi

echo "----------------------------------------------------"
echo "MLDep: Adding backends to loadbalancer"
echo "----------------------------------------------------"

set -x

cd ../loadbalancer

cp fresh-to-mod.cfg mod-config.cfg

# python3 config-generator.py --model $model --container $container_deploy --container_weight $container_weight --container_instances $container_instances --vm $vm_deploy --vm_weight $vm_weight --vm_instances $vm_instances --func $function_deploy --func_weight $function_weight

python3 config-generator.py \
    --model $model \
    --container $container_deploy \
    --container_weight $container_weight \
    --container_instances $container_instances \
    --vm $vm_deploy \
    --vm_weight $vm_weight \
    --vm_instances $vm_instances \
    --func $function_deploy \
    --func_weight $function_weight \
    --func_instances $function_instances

cp mod-config.cfg haproxy.cfg 

echo "" >> haproxy.cfg

$lb_perm_string docker kill -s HUP haproxy

set +x

echo "--------------------------------------------------------"
echo "MLDep: Deployed at http://localhost:6000/predict"
echo "LoadBalancer stats page hosted at http://localhost:8404"
echo "--------------------------------------------------------"