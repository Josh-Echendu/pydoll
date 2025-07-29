import asyncio
from pydoll.commands.dom_commands import DomCommands

async def wait_for_query_selector(tab, node_id, selector, timeout=10, interval=0.5):
    command = DomCommands.query_selector(node_id=node_id, selector=selector)

    # Try repeatedly until timeout is reached
    for _ in range(int(timeout / interval)):
        result = await tab._connection_handler.execute_command(command)
        node = result['result'].get("nodeId")
        if node:
            return node  # Element found!
        await asyncio.sleep(interval)

    raise TimeoutError(f"Element '{selector}' not found within {timeout} seconds.")


# Get the root document node
doc_node = await tab.get_document()

# Wait for a specific element
node_id = await wait_for_query_selector(
    tab,
    node_id=doc_node['nodeId'],
    selector="div#main",
    timeout=10
)
print("Element node ID:", node_id)
