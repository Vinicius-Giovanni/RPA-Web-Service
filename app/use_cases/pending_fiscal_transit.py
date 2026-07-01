import asyncio
from pathlib import Path
from uuid import uuid4
import argparse

from app.services.transit_fiscal import TransitFiscal
from core.logging.log import ExecutionLogger
from settings.paths import PENDING_FISCAL_HISTORICO_PARQUET, PENDING_FISCAL_DESTINO_CSV, PENDING_FISCAL_DESTINO_TXT, PENDING_FISCAL_ORIGEM_TXT

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="pending_fiscal_transit",
        execution_id=execution_id
)

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Processa pendências de trânsito fiscal a partir de TXT e atualiza o histórico Parquet."
    )
    origem_txt = PENDING_FISCAL_ORIGEM_TXT
    destino_txt = PENDING_FISCAL_DESTINO_TXT
    destino_csv = PENDING_FISCAL_DESTINO_CSV
    historico_parquet = PENDING_FISCAL_HISTORICO_PARQUET

    parser.add_argument("--origem-txt", type=Path, default=origem_txt, required=origem_txt is None)
    parser.add_argument("--destino-txt", type=Path, default=destino_txt, required=destino_txt is None)
    parser.add_argument("--destino-csv", type=Path, default=destino_csv, required=destino_csv is None)
    parser.add_argument("--historico-parquet", type=Path, default=historico_parquet, required=historico_parquet is None)
    return parser

async def execute_pendind_fiscal_transit(
        origem_txt: str | Path,
        destino_txt: str | Path,
        destino_csv: str | Path,
        historico_parquet: str | Path,
):
    service = TransitFiscal(
        origem_txt=origem_txt,
        destino_txt=destino_txt,
        destino_csv=destino_csv,
        historico_parquet=historico_parquet
    )

    result = await service.execute()

    await logger.info(str(result))
    return result

async def _main_test() -> None:
    args = _build_parser().parse_args()
    try:
        result = await execute_pendind_fiscal_transit(
            origem_txt=args.origem_txt,
            destino_txt=args.destino_txt,
            destino_csv=args.destino_csv,
            historico_parquet=args.historico_parquet,
        )
    except Exception as exc:
        await logger.error(f'Falha ao executar pending_fiscal_transit: {exc}')
        raise

    print(result)

if __name__ == "__main__":
    asyncio.run(_main_test())