import requests
from concurrent.futures import ThreadPoolExecutor
import time
import csv
import json
import os
import random
import base64

url = 'http://localhost:5000/predict'
images_dir = "data/images/"


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

    print("Wait times for the first minute:")
    for row in reader:
        row = [int(element) for element in row]
        print(row)
        break

    for row in reader:
        if row is None:
            print("None detected, inserting empty row")
            row = []
        else:
            row = [element for element in row]
        wait_times.append(row)

# data = json.dumps({
#   "data": "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"
# })

for oneM_waits in wait_times:

    print("Number of requests being sent this minute:",len(oneM_waits))

    for wait_time in oneM_waits:
        img_data = load_random_image(images_dir)
        img_data = encode_image_to_base64(img_data)
        data = json.dumps({
            "data":img_data
            })
        pool.submit(sender, data)
        time.sleep(int(wait_time)/1000)

    break