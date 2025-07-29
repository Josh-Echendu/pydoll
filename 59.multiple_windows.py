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

        # STEP 1: Store all target IDs BEFORE clicking the popup link
        get_targets_cmd = TargetCommands.get_targets()
        before_targets = await tab._connection_handler.execute_command(get_targets_cmd)
        print('before: ', before_targets)
        print()

        # Extract only the targetIds from the response.
        before_result_target_infos = before_targets['result']["targetInfos"]
        before_ids = {t['targetId'] for t in before_result_target_infos}
        print("only IDS: ", before_ids)

        # STEP 2: Find and click the popup link
        popup_link = await tab.find(text='Open a popup window', tag_name='a')
        await popup_link.click()

        # Wait for the popup to fully open
        await asyncio.sleep(5)
        print()
        
        # Ask Chrome again: "Now tell me all targets that exist (tabs, popups)."
        after_cmd = TargetCommands.get_targets()
        after_result = await tab._connection_handler.execute_command(after_cmd)
        print("after_result: ", after_result)

        new_target_id = None

        # Get the new list of target details.
        after_result_target_infos = after_result['result']['targetInfos']
        
        for t in after_result_target_infos:
            if t['targetId'] not in before_ids:
                new_target_id = t['targetId']
                break

        print("new_target: ", new_target_id)

        print()

        # 👉 You can’t control the popup until you attach to it. This command tells Chrome: “I want to start listening and talking to this new tab.”
        attach_cmd = TargetCommands.attach_to_target(target_id=new_target_id, flatten=True) # The flatten=True means we want a simple flat session ID for communication (this is the newer and preferred method).
        attach_result = await tab._connection_handler.execute_command(attach_cmd)
        
        # 👉 Save that session ID so we can send commands to the popup window.
        session_id = attach_result['result']['sessionId']

        # 👉 This brings the popup window to the foreground (makes it active or focused).
        activate_cmd = TargetCommands.activate_target(new_target_id)
        await tab._connection_handler.execute_command(activate_cmd)

        js_cmd = RuntimeCommands.evaluate(
            expression='document.querySelector("h3")?.innerText',
            return_by_value=True
        )

        # Inject sessionId manually
        js_cmd["sessionId"] = session_id
        js_result = await tab._connection_handler.execute_command(js_cmd)
        print(js_result)
        print("Popup <h3> text:", js_result['result']['result']['value'])


        close_cmd = TargetCommands.close_target(target_id=new_target_id)
        await tab._connection_handler.execute_command(close_cmd)














            # popup_session_id = attach_result['result']['sessionId']

        # activate_cmd = TargetCommands.activate_target(popup_target)
        # await parent_tab._connection_handler.execute_command(activate_cmd)
        # js_cmd = RuntimeCommands.evaluate(

        # )


        await asyncio.sleep(2)
        await tab.close()

if __name__ == "__main__":
    asyncio.run(main())
