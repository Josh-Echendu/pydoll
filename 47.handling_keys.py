from authentication import email, password
from pydoll.browser import Chrome
from pydoll.constants import By
import asyncio
import time
from pydoll.commands.input_commands import InputCommands



async def pydoll_login():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://tutorialsninja.com/demo/index.php?route=account/login")

        # Wait for the email and password input fields
        email_field = await tab.find_or_wait_element(By.ID, "input-email", timeout=10)
        password_field = await tab.find_or_wait_element(By.ID, "input-password", timeout=10)

        # Type email and password
        await email_field.type_text(email)
        await password_field.type_text(password)

        # Press ENTER while focused on password field
        key_down = InputCommands.dispatch_key_event(
            type='keyDown',
            key='Enter'
        )

        key_up = InputCommands.dispatch_key_event(
            type='keyUp',
            key='Enter'
        )

        await tab._connection_handler.execute_command(key_down)
        await tab._connection_handler.execute_command(key_up)

        # Optional: wait for the next page to load
        await asyncio.sleep(5)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(pydoll_login())
