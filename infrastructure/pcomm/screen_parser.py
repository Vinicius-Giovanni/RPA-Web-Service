"""
Responsável por interpretar o texto bruto extraído da tela 3270 (via PcommClient)
e tranformá-lo em dados estruturados (dict/campos nomeados)

Este módulo não conhece regra de negócio de enriquecimento - apenas sabe
'onde' cada campo está na tela e como extraí-lo

A definição de posições (linha, coluna, tamanho) fica centralizada em
'FieldPosition', facilitando manutenção caso o layout da tela mude.
"""

from dataclasses import dataclass
from typing import Dict, List

from infrastructure.pcomm.client import PcommClient

from core.logging.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="pcomm_session_validator",
        execution_id=execution_id
)

@dataclass(fronze=True)
class FieldPosition:
    """
    Define a posição de um campo na tela 3270 (coordenadas 1-based)
    """

    name: str
    row: int
    column: int
    length: int

class ScreenParser:
    """
    Extrai campos nomeados da tela do PCOMM com base em um mapeameno
    de posições (linha/coluna/tamanho).

    Uso:
        parser = ScreenParser(client)
        parser.set_field_map([
        FieldPosition(name='codigo_cliente', row=6, column=20, length=10),
        FieldPosition(name='status', row=8, column=20, length=15),
        ])
        dados = parser.extract_fields()
    """

    def __init__(self, client: PcommClient):
        self._client = client
        self._field_map: List[FieldPosition] = []

    # Configuração do mapeamento de campos

    async def set_field_map(self, field_positions: List[FieldPosition]) -> None:
        """
        Define o layout de campos a serem extraidos da tela atual.
        """
        self._field_map = field_positions
    
    async def add_field(self, name: str, row: int, column: int, length: int) -> None:
        """
        Adiciona um único campo ao mapeamento
        """
        self._field_map.append(FieldPosition(name=name, row=row, column=column, length=length))

    # Extração

    async def extract_fields(self) -> Dict[str, str]:
        """
        Lê cada campo definido no mapeamento diretamente da tela (via cliente)
        e retorna um dicionário {nome_campo: valor}
        """
        if not self._field_map:
            await logger.warning('Nenhum mapeamento de campo definido. Use set_field_map() ou add_field()')

        result: Dict[str, str] = {}
        for field in self._field_map:
            try:
                raw_value = self._client.read_field(field.row, field.column, field.length)
                result[field.name] = raw_value.strip()
            except Exception as e: # noqa: BLE001
                await logger.warning('Falha ao extrair campo "%s": %s', field.name, e)
                result[field.name] = ""
        
        await logger.info('Campos extraídos da tela: %s', result)
        return result
    
    # Utilitarios de leitura bruta/ diagnóstico

    async def extract_full_screen(self) -> str:
        """
        Retorna o texto bruto completo da tela (útil para debug ou parsisg manual)
        """
        return self._client.read_screen_text()
    
    async def extract_full_screen_lines(self) -> List[str]:
        """
        Retorna a tela como lista de linhas, útil para localizar campos dinamicamente
        """
        return self._client.read_screen_text().split("\n")
    
    async def find_line_containing(self, text: str) -> str:
        """
        Localiza e retorna a primeira linha da tela que contém o texto informado.
        útil para telas cujo layout de campos pode varias (ex: mensagens de erro)
        """
        for line in self.extract_full_screen_lines():
            if text in line:
                return line.strip()
        return ""
    
    async def screen_contains(self, text: str) -> bool:
        """
        Verifica se um determinado texto está presente em qualquer lugar da tela
        """
        return text in self.extract_full_screen()