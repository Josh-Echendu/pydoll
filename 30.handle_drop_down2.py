
import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions

async def check_button_enabled():
    options = ChromiumOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920,1080")

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("https://1xbet.whoscored.com/regions/252/tournaments/2/england-premier-league")
        await asyncio.sleep(3)

        drop_down = await tab.find_or_wait_element(By.ID, "tournaments")
        await drop_down.click()
        await asyncio.sleep(2)
        
        shields = await tab.find_or_wait_element(By.XPATH, "//select[@id='tournaments']/option", find_all=True)

        for i,shield in enumerate(shields):
            print(i+1, ': ', shield.get_attribute("value"))

        await asyncio.sleep(2)

        await tab.execute_script("history.back()")

        await shield.click()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(check_button_enabled())
