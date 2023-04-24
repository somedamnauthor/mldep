import os

image_path = 'input/images/'

images = os.listdir(image_path)
for i in range(len(images)):
    images[i] = image_path+images[i]

for image in images:
    os.system('python3 alexnet_code.py '+image+' input/imagenet_classes.txt')