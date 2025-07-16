import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions

async def check_button_enabled():
    # Initialize Chrome with specific window size options
    options = ChromiumOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920,1080")

    # Launch browser using PyDoll's Chrome context manager
    async with Chrome(options=options) as browser:
        tab = await browser.start()

        # Navigate to target page
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)  # Allow page to load fully

        # Find all <option> elements inside the multiselect dropdown
        multiselection_dropdown = await tab.find_or_wait_element(
            By.XPATH,
            "//select[@id='multiselect1']/option",
            find_all=True
        )
        
        # ✅ Select option by value = 'audix'
        for option in multiselection_dropdown:
            if option.get_attribute("value") == 'audix':
                await option.click()

        # ✅ Select option by index = 1 (second option)
        await multiselection_dropdown[1].click()

        # ✅ Select option by visible text = 'Hyundai'
        for option in multiselection_dropdown:
            if await option.text == 'Hyundai':
                await option.click()


        await asyncio.sleep(2)
        await asyncio.sleep(300)  # For manual inspection if needed

# Entrypoint for async execution
if __name__ == "__main__":
    asyncio.run(check_button_enabled())
