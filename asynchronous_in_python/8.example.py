#| Option                            | What it does                                |
#| --------------------------------- | ------------------------------------------- |
#| `asyncio.FIRST_COMPLETED`         | Returns as soon as **any task is done**     |
#| `asyncio.FIRST_EXCEPTION`         | Returns if **any task raises an exception** |
#| `asyncio.ALL_COMPLETED` (default) | Waits for **all tasks**                     |


import asyncio

async def task(name, delay):
    try:
        await asyncio.sleep(delay)
        print(f"{name} finished")
        return name
    
    # If the task is cancelled (with .cancel()), this part runs instead of finishing the task.
    except asyncio.CancelledError:
        print(f"{name} was cancelled")
        return None


async def main():
    tasks = [
        # You create 3 tasks and run them immediately in the background.
        asyncio.create_task(task("Task A", 3)),
        asyncio.create_task(task("Task B", 1)),
        asyncio.create_task(task("Task C", 2)),
    ]

    # This line pauses until the first task is done (FIRST_COMPLETED).
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    # done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    
    print("Done tasks: ")
    for d in done:
        # wait to get the returned value
        print(await d)

    # You go through the tasks that are not done yet and call .cancel() on them.
    print("cancelled Pending task: ")
    for p in pending:
        p.cancel()

    # This waits for the cancelled tasks to handle the cancellation properly.
    await asyncio.gather(*pending, return_exceptions=True) # return_exceptions=True, avoids crashing if they raise errors (like CancelledError).


asyncio.run(main())
