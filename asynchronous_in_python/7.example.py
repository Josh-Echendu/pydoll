#| Option                            | What it does                                |
#| --------------------------------- | ------------------------------------------- |
#| `asyncio.FIRST_COMPLETED`         | Returns as soon as **any task is done**     |
#| `asyncio.FIRST_EXCEPTION`         | Returns if **any task raises an exception** |
#| `asyncio.ALL_COMPLETED` (default) | Waits for **all tasks**                     |


import asyncio

async def task(name, delay):
    await asyncio.sleep(delay)
    print(f"{name} finished")
    return name

async def main():
    tasks = [
        asyncio.create_task(task("Task A", 3)),
        asyncio.create_task(task("Task B", 1)),
        asyncio.create_task(task("Task C", 2)),
    ]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    # done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    print("Done tasks: ")
    for d in done:
        print(await d)

    print("Pending task: ")
    for p in pending:
        print(p)

asyncio.run(main())
