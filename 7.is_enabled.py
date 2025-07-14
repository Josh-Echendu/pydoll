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
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)

        button = await tab.find_or_wait_element(By.ID, "but1", raise_exc=True, find_all=False)
        print(button)

        #<button disabled> ... </button>  <!-- Disabled -->
        #<button disabled=""> ... </button>  <!-- Disabled -->
        #<button disabled="true"> ... </button>  <!-- Still Disabled -->

        disabled_atribute = button.get_attribute('disabled')
        if disabled_atribute == '':
            print("Disabled")

        else:
            print("Enabled")

        await asyncio.sleep(5)
        await tab.close()


if __name__ == "__main__":
    asyncio.run(check_button_enabled())


