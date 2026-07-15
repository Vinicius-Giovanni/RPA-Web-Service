from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv
import asyncio

from app.use_cases.extract_cookies_ibm_login import ExtractCookiesLogin
from settings.paths import ENV_PATH, COOKIES_FILE
from settings.chromium_settings import start_browser

load_dotenv(dotenv_path=ENV_PATH)

async def extrack_cookies_ibm():

    async with async_playwright() as p:

        playwright, browser, page = await start_browser()

        await ExtractCookiesLogin.login(
            page=page,
            email=os.getenv('MANAGER_EMAIL'),
            password=os.getenv('PASSWORD'),
            dir_cookies=COOKIES_FILE
        )

        input('Pressione Enter para fechar')

        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    asyncio.run(extrack_cookies_ibm())