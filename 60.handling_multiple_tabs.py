import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.target_commands import TargetCommands
from pydoll.commands.runtime_commands import RuntimeCommands
from pydoll.commands.page_commands import PageCommands



async def main():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)
    
        before_cmd = TargetCommands.get_targets()
        before_result = await tab._connection_handler.execute_command(before_cmd)
        print(before_result)

        before_ids = {t['targetId'] for t in before_result['result']['targetInfos']}
        print(before_ids)

        await (await tab.find(id='link2')).click()
        await asyncio.sleep(2)

        after_cmd = TargetCommands.get_targets()
        after_result = await tab._connection_handler.execute_command(after_cmd)
        print()
        print(after_result)        
        new_target_id = None
        for t in after_result['result']['targetInfos']:
            if t['targetId'] not in before_ids and t['type'] == 'page':
                new_target_id = t['targetId']
                break

        attach_cmd = TargetCommands.attach_to_target(target_id=new_target_id, flatten=True)
        attach_result = await tab._connection_handler.execute_command(attach_cmd)
        session_id = attach_result['result']['sessionId']
        print(attach_result)

        activate_cmd = TargetCommands.activate_target(new_target_id)
        await tab._connection_handler.execute_command(activate_cmd)

        # Click an item in the new popup page , window or tab
        link_cmd = RuntimeCommands.evaluate(
            expression="document.querySelector('a[href='http://selenium-by-arun.blogspot.com/2012/11/what-is-selenium.html']')?.click()",
            return_by_value=True
        )
        link_cmd['sessionId'] = session_id
        link_result = await tab._connection_handler.execute_command(link_cmd)
        print(link_result)

        await asyncio.sleep(3)

        close_cmd = TargetCommands.close_target(target_id=new_target_id)
        await tab._connection_handler.execute_command(close_cmd)

        await asyncio.sleep(3)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(main())


🧭 Next Step: Want to move to waiting mechanisms now (e.g., find_or_wait_element, manual Runtime.evaluate(... while loop), timeouts)?
Let me know your goal — wait for page loads, element appearance, AJAX data, etc.
I'll tailor the lesson just for what you need.
