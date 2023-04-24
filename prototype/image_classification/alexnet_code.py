# Imports

from torchvision import models
import torch
from torchvision import transforms
from PIL import Image
import os
import sys
import warnings
warnings.filterwarnings("ignore")

# Input

class Model:

    def model_definition(self):

        alexnet = models.alexnet(pretrained=True)
        alexnet.eval()
        return alexnet


    def preprocess_input(self, image_path):
     
        transform = transforms.Compose([            #[1]
         transforms.Resize(256),                    #[2]
         transforms.CenterCrop(224),                #[3]
         transforms.ToTensor(),                     #[4]
         transforms.Normalize(                      #[5]
         mean=[0.485, 0.456, 0.406],                #[6]
         std=[0.229, 0.224, 0.225]                  #[7]
         )])

        img = Image.open(image_path)
        img_t = transform(img)
        batch_t = torch.unsqueeze(img_t, 0)

        return batch_t


    def predict(self, model, batch_t, classes_path):

        with open(classes_path) as f:
            classes = [line.strip() for line in f.readlines()]

        out = model(batch_t)
        _, index = torch.max(out, 1)
        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
        # print(classes[index[0].item()], percentage[index[0]].item())

        return classes[index[0].item()]


# model = Model()

# alexnet = model.model_definition()

# image_path = sys.argv[1]
# batch_t = model.preprocess_input(image_path)

# classes_path = sys.argv[2]
# prediction = model.predict(alexnet, batch_t, classes_path)
# print(prediction)