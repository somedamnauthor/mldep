import aiohttp
import asyncio
import time

wait_times = [2, 2, 2, 2, 2, 2, 2, 2, 2]  # Example list of wait times in seconds

async def get_prediction(session, url, wait_time):
    start_time = time.time()  # Start time for each request
    async with session.post(url, data={'data': 'My heart! I [MASK] her!'}) as resp:
        prediction = await resp.json()
        response_time = time.time() - start_time  # Calculate response time
        print(f"Response time: {response_time} seconds")
        return prediction

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for wait_time in wait_times:
            url = 'http://localhost:5000/predict'
            tasks.append(asyncio.ensure_future(get_prediction(session, url, wait_time)))
            time.sleep(wait_time)

        await asyncio.gather(*tasks)

asyncio.run(main())