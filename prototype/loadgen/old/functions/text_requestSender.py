import requests
from concurrent.futures import ThreadPoolExecutor
import time
import csv
import json
import os
import random

url = 'http://localhost:6000/predict'
contexts = "data/context/masked_sentences.txt"
# contexts = "data/prompts/sentences.txt"

# Read the contents of 'masked_sentences.txt' into a list
with open(contexts, 'r') as file:
    sentences = file.readlines()

# Remove leading/trailing whitespaces and newlines from each sentence
sentences = [sentence.strip() for sentence in sentences]


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


# Variable to control how many minutes the loadgen should run for
loadgen_length = 60
counter = 0

for oneM_waits in wait_times:

    # print("Number of requests being sent this minute:",len(oneM_waits))

    for wait_time in oneM_waits:
        
        data = json.dumps({
            "data":random.choice(sentences)
            })
        pool.submit(sender, data)
        time.sleep(int(wait_time)/1000)

    if counter == loadgen_length:
        break