from __future__ import annotations

import asyncio

from app.use_cases.pcom_extract_acertos import ExecutePcommExtractAcertos

async def run_pcom():

    executor = ExecutePcommExtractAcertos()

    await asyncio.to_thread(
        executor.execute
    )

if __name__ == "__main__":
    asyncio.run(run_pcom())