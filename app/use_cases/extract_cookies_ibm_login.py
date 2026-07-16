from pathlib import Path
import json
import os


from settings.elements_ibm import LINKS, ELEMENTS_LOGIN
from settings.paths import COOKIES_FILE
from core.logging.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="dataframe_manager",
        execution_id=execution_id
)

class ExtractCookiesLogin:

    @staticmethod
    async def login(page, email: str, password: str, dir_cookies: str | Path) -> list[dict]:

        # > Site
        await page.goto(LINKS['LOGIN'])

        # validate start window
        await page.locator(ELEMENTS_LOGIN['window_validation_login']).wait_for()

        # Dropdown Azure AD select
        await page.locator(
            ELEMENTS_LOGIN['namespace_dropdown_button']
        ).click()

        # Dropdown select namespace
        await logger.info('Tela de extração de cookies validada')

        # Select Azure AD
        await page.locator(
            ELEMENTS_LOGIN['namespace_azuread']
        ).click()

        # Banner Microsoft
        await page.locator(
            ELEMENTS_LOGIN['element_banner']
        ).wait_for()

        # Send Email
        await page.fill(
            ELEMENTS_LOGIN['email'],
            os.getenv('MANAGER_EMAIL')
        )

        # Confirm Email
        await page.click(
            ELEMENTS_LOGIN['submit_button']
        )

        # Send Password
        await page.fill(
            ELEMENTS_LOGIN['password'],
            os.getenv('PASSWORD')
        )

        # Confirm Password
        await page.click(
            ELEMENTS_LOGIN['submit_button']
        )

        # Connected
        await page.click(
            ELEMENTS_LOGIN['submit_button']
        )

        # validate pattern window
        await page.locator(
            ELEMENTS_LOGIN['element_button']
        ).wait_for()

        cookies = await page.context.cookies()

        with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=4)

        return cookies

