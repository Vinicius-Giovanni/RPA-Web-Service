from __future__ import annotations

import asyncio

from app. use_cases.execute_pcom_validade_invoices import ExecutePcommExtractInvoices

async def run_pcom():

    executor = ExecutePcommExtractInvoices()

    await asyncio.to_thread(
        executor.execute_pcom
    )

if __name__ == "__main__":
    asyncio.run(run_pcom())