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
        await tab.go_to("https://practice-automation.com/modals/")
        await asyncio.sleep(3)

        simple_modal_button = await tab.find_or_wait_element(By.XPATH, "(//button[@type='button'])[1]", find_all=False, raise_exc=True, timeout=5)
        await simple_modal_button.click()

        simple_modal_text = await tab.find_or_wait_element(By.XPATH, '(//div[@class="pum-content popmake-content"])[2]/p[contains(text(), "Hi, I’m a simple modal.")]')
        print(await simple_modal_text.text)

        await asyncio.sleep(5)
        cancel_btn = await tab.find_or_wait_element(By.XPATH, "(//div[@tabindex='0']//following-sibling::button)[3]")
        await cancel_btn.click()

        await asyncio.sleep(3)









if __name__ == "__main__":
    asyncio.run(check_button_enabled())
