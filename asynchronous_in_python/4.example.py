import asyncio
import time


async def do_work(name, delay):
    await asyncio.sleep(delay)
    print(f"{name} done")

async def main():
    # This is bad and slow
    await do_work('task1', 2)
    await do_work('task2', 1)


start = time.perf_counter()
asyncio.run(main())
end = time.perf_counter()

print(f"Finished in {end - start:.6f} seconds")
