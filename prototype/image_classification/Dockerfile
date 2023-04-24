#FROM ubuntu:20.04
FROM python:3.8-buster

RUN apt update -y
#RUN apt install python3 -y
RUN apt install python3-pip -y
#RUN apk add gcc

RUN pip3 install flask

RUN pip3 install torch --find-links https://download.pytorch.org/whl/torch_stable.html
RUN apt install make automake gcc g++
RUN pip3 install torchvision --find-links https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install Pillow 

COPY . /home/ml

RUN pip3 install flask_restful

#RUN pip3 install -r /home/ml/input/requirements.txt

#ENTRYPOINT ["python3", "/home/ml/wrapper.py"]

EXPOSE 5000 
