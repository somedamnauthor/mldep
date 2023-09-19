# Imports

from torchvision import models
# import torch
# from torchvision import transforms
from PIL import Image

import base64
from io import BytesIO
import re

import os
import sys
import warnings
warnings.filterwarnings("ignore")

from torchvision.models import resnet50, ResNet50_Weights

class Model:

    def model_definition(self):

        weights = ResNet50_Weights.DEFAULT
        model = resnet50(weights=weights)
        model.eval()

        return model


    def preprocess_input(self, data):
     
        weights = ResNet50_Weights.DEFAULT
        preprocess = weights.transforms()
        
        base64img = re.sub('^data:image/.+;base64,', '', data)
        img = Image.open(BytesIO(base64.b64decode(base64img)))

        batch = preprocess(img).unsqueeze(0)

        return batch


    def predict(self, model, batch):

        weights = ResNet50_Weights.DEFAULT

        prediction = model(batch).squeeze(0).softmax(0)

        class_id = prediction.argmax().item()
        score = prediction[class_id].item()
        category_name = weights.meta["categories"][class_id]
        
        # print(f"{category_name}: {100 * score:.1f}%")

        return category_name


# Instantiate model
model = Model()
model_definition = model.model_definition()

from datetime import datetime
import time

def main(args):

    timestamp = datetime.utcnow().isoformat()

    # Get data
    data = args['data']

    # Call the pre-processing step and recieve pre-processed data back
    prepro_start = time.time()
    batch_t = model.preprocess_input(data)
    prepro_time = time.time() - prepro_start

    # Call the predict method using the pre-processed data
    predict_start = time.time()
    prediction = model.predict(model_definition, batch_t)
    predict_time = time.time() - predict_start
    output = {'prediction':prediction}

    out = [timestamp, prepro_time, predict_time, (prepro_time+predict_time)]

    # with open('log.csv', 'a') as file:
    #     file.write(str(out) + '\n')
            
    return {"output": [prediction, out]}
