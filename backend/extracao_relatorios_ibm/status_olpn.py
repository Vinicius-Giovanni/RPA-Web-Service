from utils.chromium_settings import start_browser
from utils.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="3.11 - Status Wave + oLPN",
        execution_id=execution_id
)

async def login_page():

        await logger.info(
                "Iniciando extração"
        )

        playwright, browser, page = await start_browser()

        url = "https://prweb01/bahia/gateway?hptAppId=W1A1&hptExec=Y"

        page.goto(url)

        page.wait_for_timeout_500
