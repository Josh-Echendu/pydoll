#| Purpose           | `create_task()`                     | `gather()`                                      |
#| ----------------- | ----------------------------------- | ----------------------------------------------- |
#| Starts a task?    | ✅ Yes, right away                   | ✅ Yes, if passed coroutine (or already running) |
#| Waits for result? | ❌ No (until you `await` it later)   | ✅ Yes — waits for **all tasks** to finish       |
#| Returns           | Task object (you can `await` later) | Final results of all tasks (as a list)          |
#| Analogy           | "Start cooking this dish now."      | "Cook all dishes together and wait until done." |


import asyncio
import time


async def do_work(name, delay):
    await asyncio.sleep(delay)
    print(f"{name} done")

async def main():
    # These tasks are now running concurrently (not sequentially).
    task1 = asyncio.create_task(do_work("Task 1", 2))
    task2 = asyncio.create_task(do_work("Task 2", 1))

    # This executes immediately, before either task finishes, because both were just scheduled — not awaited yet.
    print("Both tasks started")

# This tells the event loop:
# "Wait for task1 to finish."

# Then, "wait for task2 to finish."

# But note: task2 might already be done by the time we await it!

# Because they were both started at the same time, task2 (1 second delay) will finish first — even though await task1 is first.
    await task1
    await task2


    print("both task ended")

start = time.perf_counter()
asyncio.run(main())
end = time.perf_counter()

print(f"Finished in {end - start:.6f} seconds")