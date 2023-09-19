import requests
from concurrent.futures import ThreadPoolExecutor
import time
import csv
import json
import os
import random
import base64

url = 'http://localhost:6000/predict'
images_dir = "data/images/"
# images_dir = "data/caching/images/"


def load_random_image(images_dir):
    # Get a list of all image files in the directory
    image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]

    if not image_files:
        raise ValueError("No image files found in the directory.")

    # Pick a random image file from the list
    random_image_file = random.choice(image_files)

    # Load the image as binary data
    with open(os.path.join(images_dir, random_image_file), "rb") as image_file:
        image_data = image_file.read()

    return image_data

def encode_image_to_base64(image_data):
    # Encode the image data to base64
    base64_encoded = base64.b64encode(image_data).decode("utf-8")
    return base64_encoded


pool = ThreadPoolExecutor(100)

sender = lambda data: requests.post(
    url,
    headers={'Content-Type': 'application/json'},
    data=data
)

wait_times = []

with open('wait_times.csv', 'r') as f:
    reader = csv.DictReader(f)

    # print("Wait times for the first minute:")
    # for row in reader:
    #     row = [int(element) for element in row]
    #     print(row)
    #     break

    for row in reader:
        if row is None:
            print("None detected, inserting empty row")
            row = []
        else:
            row = [element for element in row]
        wait_times.append(row)


# Variable to control how many minutes the loadgen should run for
loadgen_length = 60
counter = 0

for oneM_waits in wait_times:

    counter = counter + 1

    print("Number of requests being sent this minute:",len(oneM_waits))

    for wait_time in oneM_waits:
        img_data = load_random_image(images_dir)
        img_data = encode_image_to_base64(img_data)
        data = json.dumps({
            "data":img_data
            })
        pool.submit(sender, data)
        time.sleep(int(wait_time)/1000)

    #break

    if counter == loadgen_length:
        break