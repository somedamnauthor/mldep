# Sample usage: sh mldep.sh -m bert -c true -f true -v false

echo "----------------------------------------------------"
echo "MLDep: Starting HAProxy with initial config"
echo "----------------------------------------------------"

set -x

cd ../loadbalancer

sh deploy_lb.sh

set +x

# Parse the command-line options using getopts
while getopts "m:c:f:v:" opt; do
  case $opt in
  	m) model="$OPTARG" ;;
    c) container="$OPTARG" ;;
    f) func="$OPTARG" ;;
    v) vm="$OPTARG" ;;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
  esac
done

# # Your script code here
# echo "Container: $container"
# echo "Func: $func"
# echo "VM: $vm"

echo "----------------------------------------------------"
echo "MLDep: Checking for Container Deployment"
echo "----------------------------------------------------"

if [ "$container" = "true" ]; then
  cd ../Container
  sh container_wrapper.sh $model
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

if [ "$func" = "true" ]; then
  cd ../Functions
  sh function_deploy.sh /home/srishankar/openwhisk $model
fi

echo "----------------------------------------------------"
echo "MLDep: Adding backends to loadbalancer"
echo "----------------------------------------------------"

set -x

cd ../loadbalancer

cp fresh-to-mod.cfg mod-config.cfg

python3 config-generator.py --model $model --container $container --vm $vm --func $func

cp mod-config.cfg haproxy.cfg 

echo "" >> haproxy.cfg

sudo docker kill -s HUP haproxy

set +x

echo "--------------------------------------------------------"
echo "MLDep: Deployed at http://localhost:6000/predict"
echo "LoadBalancer stats page hosted at http://localhost:8404"
echo "--------------------------------------------------------"