from app.services.transit_fiscal import TransitFiscal
from utils.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="pending_fiscal_transit",
        execution_id=execution_id
)


service = TransitFiscal(
    origem_txt=...,
    destino_txt=...,
    destino_csv=...,
    historico_csv=...
)

result = service.execute()

logger.info(result)