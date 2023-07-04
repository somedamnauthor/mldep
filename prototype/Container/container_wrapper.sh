cp Dockerfile ../image_classification/Dockerfile

cd ../image_classification

sudo docker build -t image_classifier .

sudo docker run -d -p 5000:5000 image_classifier

rm Dockerfile
