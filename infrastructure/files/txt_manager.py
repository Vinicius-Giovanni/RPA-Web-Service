import csv
from datetime import datetime
from pathlib import Path
from settings.settings import get_type_filial, DELIMITADOR_TXT_MANAGER
from core.logging.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="txt_manager",
        execution_id=execution_id
)

class TxtManager:

    DELIMITADOR = DELIMITADOR_TXT_MANAGER

    async def process(
            self,
            file_txt: str,
            file_csv: str,
            encoding: str = "utf-8"
    ) -> None:
        
        with open(
            file_txt,
            "r",
            encoding=encoding
        ) as infile:
            
            lines = infile.readlines()
        
        if not lines:
            await logger.error("Arquivo TXT vazio")
            raise ValueError("Arquivo TXT vazio")

        header = (
            lines[0].strip().split(self.DELIMITADOR)
        )

        header = [c.strip() for c in header]

        id_date = header.index("DT_EMI")
        id_filial_emi = header.index("FILIAL_EMI")
        id_filial_dst = header.index("FILIAL_DST")

        header.append("TIPO_FLUXO")

        Path(file_csv).parent.mkdir(parents=True, exist_ok=True)

        with open(
            file_csv,
            'w',
            newline="",
            encoding=encoding
        ) as outfile:
            
            writer = csv.writer(
                outfile,
                delimiter=self.DELIMITADOR
            )

            writer.writerow(header)

            for line in lines[1:]:
                line = line.strip()

                if not line:
                    continue

                data = [
                    d.strip()
                    for d in line.split(
                        self.DELIMITADOR
                    )
                ]

                if len(data) < len(header) - 1:
                    continue

                data = data[:len(header) - 1]

                try:
                    data[id_date] = (
                        datetime.strptime(
                            data[id_date],
                            "%d.%m.%Y"
                        ). strftime("%Y-%m-%d")
                    )
                except ValueError:
                    data[id_date] = None
                
                type_emi = await get_type_filial(
                    data[id_filial_emi]
                )

                type_dst = await get_type_filial(
                    data[id_filial_dst]
                )

                data.append(
                    f"{type_emi}-{type_dst}"
                )

                writer.writerow(data)