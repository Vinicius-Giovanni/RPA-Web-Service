from pathlib import Path
import json

from settings.elements_ibm import LINKS, ELEMENTS_LOGIN
from core.logging.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="dataframe_manager",
        execution_id=execution_id
)


class ExtractCookiesLogin:

    async def login(page, email: str, password: str, dir_cookies: str | Path) -> list[dict]:

        await page.goto(LINKS['LOGIN'])

        # Tela inicial
        await page.locator(ELEMENTS_LOGIN['window_validation_login']).wait_for()
