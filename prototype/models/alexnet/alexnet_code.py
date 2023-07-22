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
import requests

class Model:

    def model_definition(self):

        try:
            classes_file_url = "https://raw.githubusercontent.com/somedamnauthor/mldep/master/prototype/models/alexnet/imagenet_classes.txt"
            classes_file = requests.get(classes_file_url)
            open('imagenet_classes.txt', 'wb').write(classes_file.content)
        except:
            pass

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

        # dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = sys.path[0]
        classes_path = dir_path + "/imagenet_classes.txt"

        try:
            with open(classes_path) as f:
                classes = [line.strip() for line in f.readlines()]
        except:
            return "ERROR, couldn't find classes file"

        out = model(batch_t)
        _, index = torch.max(out, 1)
        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

        return classes[index[0].item()]
