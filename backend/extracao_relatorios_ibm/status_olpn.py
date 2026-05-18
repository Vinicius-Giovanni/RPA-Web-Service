from utils.chromium_settings import start_browser



async def login_page():

        playwright, browser, page = await start_browser()

        url = "https://prweb01/bahia/gateway?hptAppId=W1A1&hptExec=Y"

        page.goto(url)

        page.wait_for_timeout_500
