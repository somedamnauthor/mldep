import aiohttp
import asyncio
import time

# Define the endpoint URL
endpoint_url = 'http://localhost:6000/predict'  # Replace with your endpoint URL

# Define the list of requests per minute (reqs) and the total number of requests
reqs = [30]  # Change this list to your desired request rates
total_requests = sum(reqs)

# Define the headers (if needed)
headers = {'Content-Type': 'application/json'}

# Function to send requests asynchronously and record latency
async def send_requests_async(requests_per_minute):

    async with aiohttp.ClientSession(headers=headers) as session:
        for i in range(requests_per_minute):
            start_time = time.time()

            # Send an HTTP GET request to the endpoint asynchronously
            async with session.get(endpoint_url) as response:
                end_time = time.time()
                latency = end_time - start_time

                # Print or log the latency for each request
                print(f'Request {i + 1}/{requests_per_minute}: Latency = {latency:.4f} seconds')

# Asynchronously send requests for each specified request rate
async def main():
    for req in reqs:
        await send_requests_async(req)

if __name__ == '__main__':
    asyncio.run(main())

print(f'Total requests sent: {total_requests}')
