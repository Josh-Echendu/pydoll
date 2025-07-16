
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
        
        shield = await tab.find_or_wait_element(By.XPATH, "//select/option[@value='/Regions/252/Tournaments/8/england-league-one']")
        await shield.click()

        await asyncio.sleep(2)

        await tab.execute_script("history.back()")

        await shield.click()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(check_button_enabled())
