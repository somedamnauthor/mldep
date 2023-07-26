FROM python:3.8-buster

RUN apt update -y

RUN apt install python3-pip -y

RUN pip3 install flask

RUN pip3 install flask_restful

RUN pip3 install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html

RUN apt install make automake gcc g++

RUN pip3 install Pillow 

COPY . /home/ml

RUN pip3 install -r /home/ml/requirements.txt

EXPOSE 5000

CMD python3 /home/ml/wrapper.py
