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

        from transformers import pipeline
        unmasker = pipeline('fill-mask', model='bert-base-uncased')

        return unmasker


    def preprocess_input(self, data):
     
        return data


    def predict(self, model, batch_t):

        prediction = model(batch_t)[0]['token_str']

        return prediction

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
