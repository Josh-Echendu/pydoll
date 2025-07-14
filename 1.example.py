import asyncio
from pydoll.constants import By
from pydoll.browser import Chrome

# async def automate_omayo_with_pydoll():
#     async with Chrome() as browser:
#         tab = await browser.start()
#         await tab.go_to("http://omayo.blogspot.com")
#         await asyncio.sleep(5)
#         drop_down = await tab.find(class_name='dropbtn')
#         await drop_down.click()

# async def automate_omayo_with_pydoll():
#     async with Chrome() as browser:
#         tab = await browser.start()
#         await tab.go_to("http://omayo.blogspot.com")
#         await asyncio.sleep(5)
#         link = await tab.find(text='compendiumdev')
#         await link.click()
#         await asyncio.sleep(5)


# async def automate_whoscored_with_pydoll():
#     async with Chrome() as browser:
#         # Get the initial tab to interact with the browser page.
#         tab = await browser.start()

#         await tab.go_to("https://1xbet.whoscored.com/")
#         await asyncio.sleep(2) # A small additional pause for rendering stability

        # input_port = await tab.query("//button[@id='Top-Tournaments-btn']/span[normalize-space()='Top Tournaments']")
        # input_port = await tab.find_or_wait_element(By.XPATH, "//button[@id='Top-Tournaments-btn']/span[normalize-space()='Top Tournaments']", find_all=False, timeout=5, raise_exc=True)

#         await input_port.click()
#         await asyncio.sleep(5) # Allow the action to complete and any new content to load

async def automate_whoscored_with_pydoll():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://1xbet.whoscored.com/")
        await asyncio.sleep(2)

        # Find and click on 'Match Centre'
        livescore = await tab.find_or_wait_element(text='Match Centre', timeout=5)
        livescore = await tab.find_or_wait_element(By.LINK_TEXT, 'Match Centre', timeout=8)


        await livescore.click()

        await asyncio.sleep(5)


# Entry point for running the asynchronous function.
if __name__ == "__main__":
    asyncio.run(automate_whoscored_with_pydoll())

# element = await tab.query("//button[@id='submit']")
# elements = await tab.query("//div[@class='item']", find_all=True)
# element = await tab.query("//button[text()='Submit']", timeout=10)


