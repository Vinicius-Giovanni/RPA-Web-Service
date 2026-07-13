from __future__ import annotations

import asyncio

from app. use_cases.execute_pcom_validade_invoices import execute_pcom

async def run_pcom():
    result = await asyncio.to_thread(
        execute_pcom
    )

if __name__ == "__main__":
    asyncio.run(run_pcom())