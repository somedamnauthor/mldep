#sample usage: sh container_wrapper image_classification

destination="../models/${1}"

dockerfile_path="${destination}/Dockerfile"

cp Dockerfile "$dockerfile_path"

cd "${destination}/"

pwd

sudo docker build -t "${1}" .

sudo docker run -d -p 5000:5000 "${1}"

rm Dockerfile