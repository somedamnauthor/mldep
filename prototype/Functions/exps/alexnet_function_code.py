# Imports

from torchvision import models
import torch
from torchvision import transforms
from PIL import Image

import base64
from io import BytesIO
import re

import os
import sys
import warnings
warnings.filterwarnings("ignore")



class Model:

    def model_definition(self):

        alexnet = models.alexnet(pretrained=True)
        alexnet.eval()
        return alexnet


    def preprocess_input(self, data):
     
        transform = transforms.Compose([            #[1]
         transforms.Resize(256),                    #[2]
         transforms.CenterCrop(224),                #[3]
         transforms.ToTensor(),                     #[4]
         transforms.Normalize(                      #[5]
         mean=[0.485, 0.456, 0.406],                #[6]
         std=[0.229, 0.224, 0.225]                  #[7]
         )])
        
        base64img = re.sub('^data:image/.+;base64,', '', data)
        img = Image.open(BytesIO(base64.b64decode(base64img)))

        img_t = transform(img)
        batch_t = torch.unsqueeze(img_t, 0)

        return batch_t


    def predict(self, model, batch_t):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        classes_path = dir_path + "/input/imagenet_classes.txt"

        with open(classes_path) as f:
            classes = [line.strip() for line in f.readlines()]

        out = model(batch_t)
        _, index = torch.max(out, 1)
        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

        return classes[index[0].item()]



def main(args):

    # Instantiate model
    model = Model()

    model_definition = model.model_definition()

    return {"output": args['data']}

    # timestamp = datetime.utcnow().isoformat()

    # # Get data
    # data = args['data']

    # # Call the pre-processing step and recieve pre-processed data back
    # prepro_start = time.time()
    # batch_t = model.preprocess_input(data)
    # prepro_time = time.time() - prepro_start

    # # Call the predict method using the pre-processed data
    # predict_start = time.time()
    # prediction = model.predict(model_definition, batch_t)
    # predict_time = time.time() - predict_start
    # output = {'prediction':prediction}

    # out = [timestamp, prepro_time, predict_time, (prepro_time+predict_time)]

    # # with open('log.csv', 'a') as file:
    # #     file.write(str(out) + '\n')

    # print("hi")

    # return {"output": args['data']}
            
    # return {"output": prediction}