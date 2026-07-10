import asyncio
from pathlib import Path
from uuid import uuid4
import argparse

from infrastructure.service.invoice_fiscal import TransitFiscal
from core.logging.log import ExecutionLogger
from settings.paths import PENDING_FISCAL_HISTORICO_PARQUET, PENDING_FISCAL_DESTINO_CSV, PENDING_FISCAL_DESTINO_TXT, PENDING_FISCAL_ORIGEM_TXT

"""
Ponto de entrada para o processamento das pendências de trânsito fiscal.

Este módulo disponibiliza a interface de execução da rotina de
atualização do histórico de trânsito fiscal.

As responsabilidades deste módulo incluem:

- COnfigurar os argumentos de linha de comando;
- Instanciar o serviço responsável pelo processamento;
- Executar o fluxo principal da aplicação;
- Registrar eventos de sucesso e falha durante a execução.

Toda a lógica de negócio permance encapsulada nos seriços da
camada de aplicação, enquanto este módulo atua apenas como
orquestrador da execução.
"""

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="pending_fiscal_transit",
        execution_id=execution_id
)

def _build_parser() -> argparse.ArgumentParser:
    """
    Cria o parser responsável pela leitura dos arqumentos
    da linha de comando.

    Os caminhos utilizados pela aplicação são obtidos das
    configurações padrão, podendo ser sobrescritos pelo
    usuário durante a execução.

    Returns:
        argparse.ArgumentParser:
            Parser configurado com todos os argumentos
            necessários para executar a rotina.
    """
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

async def execute_pendindg_fiscal_transit(
        origem_txt: str | Path,
        destino_txt: str | Path,
        destino_csv: str | Path,
        historico_parquet: str | Path,
):
    """
    Executa o processamento do histórico de trânsito fiscal.

    Esta função instancia o serviço responsável pela rotina,
    executa o processamento completo e registra o resultado
    da execução no sistema de logs.

    Args:
        origem_txt:
            Caminho do arquivo TXT de origem.
        
        destino_txt:
            Caminho onde será criada a cópia do arquivo
            utilizada no processamento.

        destino_csv:
            Caminho do arquivo CSV gerado a partir do TXT.

        hitorico_parquet:
            Caminho do arquivo Parquet utilizado para armazenar o histórico consolidado.

    Returns:
        dict[str, int]:
            Resumo da execução contendo a quantidade de
            registros novos, resolvidos, pendentes e o
            total presente no histórico.
    """
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
    """
    Executa a aplicaçao quando iniciada pela linha de comando.

    Esta função realiza a leitura dos argumentos fornecidos,
    executa a rotina principal e registra possíveis falhas
    durante o processamento.

    Raises:
        Exception:
            Repropaga qualquer exceção ocorrida durante a
            execução após registra-la no sistema de logs.
    """
    args = _build_parser().parse_args()
    try:
        result = await execute_pendindg_fiscal_transit(
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