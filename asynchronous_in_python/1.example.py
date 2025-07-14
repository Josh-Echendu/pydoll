import asyncio
import time

async def fetch_data(url):
    await asyncio.sleep(2)
    return f"Data from {url}"


async def main():
    urls = ['a.com', 'b.com', 'c.com']
    task = [fetch_data(url) for url in urls]
    result = await asyncio.gather(*task)
    print(result)


start = time.perf_counter()
asyncio.run(main())
end = time.perf_counter()

print(f"Finished in {end - start:.6f} seconds")


print("************************How does the event loop manage tasks?*******************************")
# Here's how the event loop works step by step:

#You give it tasks — usually coroutines (like fetch_data() or say()).

# The loop starts running, executing the first chunk of each coroutine until it hits an await.

# When a coroutine hits await, it is paused, and control returns to the event loop.

# The loop schedules other tasks to run while the first one is waiting.

# When the awaited thing is done (e.g., I/O or asyncio.sleep()), the coroutine is resumed from where it left off.

# This continues until all tasks are complete.