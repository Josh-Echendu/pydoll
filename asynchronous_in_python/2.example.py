import asyncio
import time

async def say(message, delay):
    # await asyncio.sleep(delay)
    print(message)

async def main():
    await asyncio.gather(
        say("First", 2),
        say("Second", 1),
        say("Third", 3),
    )

start = time.perf_counter()
asyncio.run(main())
end = time.perf_counter()

print(f"Finished in {end - start:.2f} seconds")
