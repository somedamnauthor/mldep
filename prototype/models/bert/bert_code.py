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