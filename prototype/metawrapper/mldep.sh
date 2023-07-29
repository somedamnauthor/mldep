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
    data = yaml.load(file, Loader=yaml.Loader)

for key, value in data.items():
    print(f"export {key}='{str(value)}'")
END
)"

# Example: Using the variables in the rest of the script
echo "Model: $model"
echo "Container: $container"
echo "Function: $function"
echo "VM: $vm"

echo "----------------------------------------------------"
echo "MLDep: Starting HAProxy with initial config"
echo "----------------------------------------------------"


set -x

cd ../loadbalancer

sh deploy_lb.sh

set +x


echo "----------------------------------------------------"
echo "MLDep: Checking for Container Deployment"
echo "----------------------------------------------------"

if [ "$container" = "true" ]; then
  cd ../Container/lightweight/
  sh container_wrapper.sh $model
  cd ..
fi

echo "----------------------------------------------------"
echo "MLDep: Checking for VM Deployment"
echo "----------------------------------------------------"

if [ "$vm" = "true" ]; then
  cd ../VM
  python3 vm_wrapper.py $model
fi

echo "----------------------------------------------------"
echo "MLDep: Checking for Function Deployment"
echo "----------------------------------------------------"

if [ "$function" = "true" ]; then
  cd ../Functions
  sh function_deploy.sh /home/srishankar/openwhisk $model
fi

echo "----------------------------------------------------"
echo "MLDep: Adding backends to loadbalancer"
echo "----------------------------------------------------"

set -x

cd ../loadbalancer

cp fresh-to-mod.cfg mod-config.cfg

python3 config-generator.py --model $model --container $container --vm $vm --func $function

cp mod-config.cfg haproxy.cfg 

echo "" >> haproxy.cfg

sudo docker kill -s HUP haproxy

set +x

echo "--------------------------------------------------------"
echo "MLDep: Deployed at http://localhost:6000/predict"
echo "LoadBalancer stats page hosted at http://localhost:8404"
echo "--------------------------------------------------------"
