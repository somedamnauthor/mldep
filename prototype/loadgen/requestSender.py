import requests
from concurrent.futures import ThreadPoolExecutor
import time
import csv

url = 'http://localhost:5000/predict'

pool = ThreadPoolExecutor(100)

sender = lambda data: requests.post(
    'http://localhost:5000/predict',
    headers={},
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

# wait_times = [1000, 3000]

data = {'data': 'My heart! I [MASK] her!'}

for oneM_waits in wait_times:

    print("Number of requests being sent this minute:",len(oneM_waits))

    # for wait_time in oneM_waits:
    #     pool.submit(sender, data)
    #     time.sleep(wait_time/1000)

    break

# print("done:",end-start)