import asyncio
from authentication import email, password
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions


async def login_tutorialsninja():
    options = ChromiumOptions()
    # options.binary_location = '/usr/bin/google-chrome-stable'
    # options.add_argument('--headless=new')
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-notifications')

    async with Chrome(options=options) as browser:
        # Start a new tab
        tab = await browser.start()
        # Go to the website
        await tab.go_to("https://tutorialsninja.com/demo/index.php?route=account/logout")

        await asyncio.sleep(5)

        # Click on 'My Account'
        my_account = await tab.find_or_wait_element(By.XPATH, "//span[text()='My Account']", find_all=False, raise_exc=True, timeout=5)
        await my_account.click()

        # Click on 'Login'
        login_link = await tab.find(text="Login", tag_name='a')
        await login_link.click()

        # Fill in email and password
        email_input = await tab.find_or_wait_element(By.ID, "input-email", find_all=False, raise_exc=True, timeout=5)
        await email_input.type_text(email)

        password_input = await tab.find_or_wait_element(By.ID, "input-password", find_all=False, raise_exc=True, timeout=5)
        await password_input.type_text(password)

        # Click Login
        login_button = await tab.find_or_wait_element(By.XPATH, "//input[@value='Login']", find_all=False, raise_exc=True)
        await login_button.click()

        await asyncio.sleep(5)

        edit_account = await tab.find(text="Edit your account information", tag_name='a')
        if edit_account._is_element_visible:
            print("Element is visible")
        else:
            print("No Element visisble")
            
        await tab.close()


if __name__ == "__main__":
    asyncio.run(login_tutorialsninja())
