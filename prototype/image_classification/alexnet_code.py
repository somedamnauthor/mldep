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

image_path = sys.argv[1]
classes_path = sys.argv[2]
with open(classes_path) as f:
    classes = [line.strip() for line in f.readlines()]
    
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


# Model import and inference

alexnet = models.alexnet(pretrained=True)
alexnet.eval()

out = alexnet(batch_t)
_, index = torch.max(out, 1)
percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

print(classes[index[0].item()], percentage[index[0]].item())