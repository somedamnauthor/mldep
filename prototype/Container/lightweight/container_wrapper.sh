#sample usage: sh container_wrapper image_classification 3 true 2
# {1}: model
# {2}: instances
# {3}: Root access
# {4}: CPUs

echo "----------------------------------------------------"
echo "Container Wrapper: Setting up"
echo "----------------------------------------------------"

if [ "$3" = "true" ]; then
    perm_string="sudo"
else
    perm_string=""
fi

if [ "$4" = 0 ]; then
    cpus_string=""
    cpuset_string=""
elif [ "$4" = 1 ]; then
    cpus_string="--cpus=1"
    cpuset_string="--cpuset-cpus=0"
else
    number=$4
    cpuset_string="--cpuset-cpus=0-$((number - 1))"
    cpus_string="--cpus=${4}"
fi

#number=${4}
#cpuset_cpus="0-$((number - 1))"

#echo "--cpus=$number --cpuset-cpus=$cpuset_cpus"

set -x

destination="../../models/${1}"

dockerfile_path="${destination}/Dockerfile"

cp Dockerfile "$dockerfile_path"

set +x

echo "----------------------------------------------------"
echo "Container Wrapper: Building Image"
echo "----------------------------------------------------"

set -x

cd "${destination}/"

$perm_string docker build -t "${1}" .

set +x

echo "----------------------------------------------------"
echo "Container Wrapper: Starting Container"
echo "----------------------------------------------------"

# sudo docker run --name "${1}" --net mldep_net -p 5000:5000 -d "${1}" 

# Loop to run the Docker command 'number' times

name="$1"
number="$2"
base_port=5000

set -x

# Loop to run the Docker command 'number' times
for i in $(seq 1 $number); do
    container_name="$name$i"
    host_port=$((base_port + i - 1))
    $perm_string docker run --name "$container_name" $cpus_string $cpuset_string --net mldep_net -p "$host_port:$base_port" -d "$1"
    # echo "Container '$container_name' is running on port '$host_port'."
done

rm Dockerfile
