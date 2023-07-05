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
        
        print(f"{category_name}: {100 * score:.1f}%")

        return category_name
