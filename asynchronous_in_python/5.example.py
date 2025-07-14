#| Purpose           | `create_task()`                     | `gather()`                                      |
#| ----------------- | ----------------------------------- | ----------------------------------------------- |
#| Starts a task?    | ✅ Yes, right away                   | ✅ Yes, if passed coroutine (or already running) |
#| Waits for result? | ❌ No (until you `await` it later)   | ✅ Yes — waits for **all tasks** to finish       |
#| Returns           | Task object (you can `await` later) | Final results of all tasks (as a list)          |
#| Analogy           | "Start cooking this dish now."      | "Cook all dishes together and wait until done." |



import asyncio
import time
import aiohttp


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
    

async def main():
    urls = [
        'https://example.com',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/1'
    ]

    async with aiohttp.ClientSession() as session:
        task = [fetch(session, url) for url in urls]
        print("task: ", task)
        start = time.perf_counter()
        results = await asyncio.gather(*task)
        end = time.perf_counter()

        for i, result in enumerate(results):
            print(f"URL {i+1} fetched ({len(result)}) bytes")

        print(f"Fetched all in {end - start:.2f} seconds")

asyncio.run(main())