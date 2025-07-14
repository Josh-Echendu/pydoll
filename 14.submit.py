import asyncio
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions
from pydoll.browser import Chrome
from authentication import email, password

async def submit_button():
    options = ChromiumOptions()

    options.add_argument('--start-maximized')
    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("https://tutorialsninja.com/demo/index.php?route=account/logout")
        await asyncio.sleep(3)

        await (await tab.find_or_wait_element(By.XPATH, "//span[text()='My Account']")).click()
        await (await tab.find(text="Login")).click()

        await (await tab.find_or_wait_element(By.ID, "input-email", find_all=False, raise_exc=True, timeout=5)).type_text(email)

        await (await tab.find_or_wait_element(By.ID, "input-password", find_all=False, raise_exc=True, timeout=5)).type_text(password)

        await tab.execute_script("document.forms[0].submit()")

        await asyncio.sleep(5)
        await tab.close()

asyncio.run(submit_button())