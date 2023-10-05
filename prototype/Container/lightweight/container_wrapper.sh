#sample usage: sh container_wrapper image_classification

echo "----------------------------------------------------"
echo "Container Wrapper: Setting up"
echo "----------------------------------------------------"

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

docker build -t "${1}" .

set +x

echo "----------------------------------------------------"
echo "Container Wrapper: Starting Container"
echo "----------------------------------------------------"

set -x

docker run --name "${1}" --net mldep_net -p 5000:5000 -d "${1}" 

rm Dockerfile
