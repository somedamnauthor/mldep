import requests
from concurrent.futures import ThreadPoolExecutor
import time
import csv
import json
import os
import random
import base64

url = 'http://localhost:6000/predict'
images_dir = "../data/images/"


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


import asyncio
import concurrent.futures

# Define your sender function and other necessary functions here

async def main():
    loop = asyncio.get_event_loop()
    responses = []  # List to store responses
    latencies = []
    
    async def send_request(wait_time):
        nonlocal responses
        
        img_data = load_random_image(images_dir)
        img_data = encode_image_to_base64(img_data)
        data = json.dumps({
            "data": img_data
        })

        # await asyncio.sleep(int(wait_time) / 1000)
        time.sleep(int(wait_time) / 1000)  # Use time.sleep() for precise wait
        start = time.time()
        response = await loop.run_in_executor(None, sender, data)  # Run sender in executor
        latency = time.time() - start
        latencies.append(latency)
        # responses.append(response.text)  # Store response
        

    # Variable to control how many minutes the loadgen should run for
    loadgen_length = 1
    counter = 0

    tasks = []

    wait_times = []

    with open('../wait_times.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row is None:
                print("None detected, inserting empty row")
                row = []
            else:
                row = [element for element in row]
            wait_times.append(row)

    for oneM_waits in wait_times:    
        counter = counter + 1
        tasks.extend(send_request(wait_time) for wait_time in oneM_waits)
        if counter == loadgen_length:
            break
    
    # Execute tasks asynchronously and gather responses
    await asyncio.gather(*tasks)

    # print(responses)
    
    # Now 'responses' list contains the responses of all requests
    # with open('responses.txt', 'w') as file:
    #     for response in responses:
    #         file.write(response + '\n')

    with open('latencies.txt', 'w') as file:
    for latency in latencies:
        file.write(latency + '\n')
    
# Run the event loop
asyncio.run(main())