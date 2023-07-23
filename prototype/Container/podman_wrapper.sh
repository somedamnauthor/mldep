#sample usage: sh container_wrapper image_classification

echo "----------------------------------------------------"
echo "Container Wrapper: Setting up"
echo "----------------------------------------------------"

set -x

destination="../models/${1}"

dockerfile_path="${destination}/Dockerfile"

cp Dockerfile "$dockerfile_path"

set +x

echo "----------------------------------------------------"
echo "Container Wrapper: Building Image"
echo "----------------------------------------------------"

set -x

cd "${destination}/"

sudo podman build -t "${1}" .

set +x

echo "----------------------------------------------------"
echo "Container Wrapper: Starting Container"
echo "----------------------------------------------------"

set -x

sudo docker run --name "${1}" --net mldep_net -d "${1}" 

rm Dockerfile

# echo "  server ${1}_container1 ${1}:5000 check" >> ../../loadbalancer/haproxy.cfg

# sudo docker kill -s HUP haproxy

# sudo docker logs -f "${1}"