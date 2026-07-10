"""
Entidades de domínio relacionadas ao processamento PCOMM

RegistroPcomm representa uma linha original vinda do arquivo Parquet
(as 3 colunas de entrada), enquanto RegistroEnriquecido representa
o mesmo registro após a consulta na tela 3270 e aplicação da regra
de negócio de enriquecimento.

Estas classes não conhecem PCOMM, Parquet, pandas ou qualquer detalhe
de infraestrutura - são objetos de domínio puros.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class RegistroPcomm:
    """
    Representa uma linha de entrada do arquivo Parquet, contendo
    as colunas necessáiras para realizar a consulta no PCOMM.

    OBS: Ajustar os campos de colunas conforme o Parque gerado
    """

    column_1: str
    column_2: str
    column_3: str

    async def is_valid(self) -> bool:
        """
        Valida se os campos mínimos neessários para consulta estão preenchidos
        """
        return bool(
            self.column_1 and self.column_1.strip()
            and self.column_2 and self.column_2.strip()
            and self.column_3 and self.column_3.strip()
        )
    
    async def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
@dataclass
class RegistroEnriquecido:
    """
    Representa o registro original acrescido dos dados obtidos via consulta
    ao PCOM e após a aplicação da regra de negócio de enriquecimento

    Mutável (não-frozen) pois é construído incrementalmente ao logo do
    pipeline (consulta => parsing => enriquecimento).
    """

    registro_origem: RegistroPcomm

    # Dados brutos extraídos da tela 3270 (chave; nome do campo, valor: texto)
    dados_tela: Dict[str, str] = field(default_factory=dict)

    valor_enriquecido: Optional[str] = None

    sucess: bool = False
    mensagem_erro: Optional[str] = None

    # Metadados de auditoria
    processado_em: Optional[datetime] = None

    async def marcar_sucesso(self, valor_enriquecido: str) -> None:
        """
        Marca o registro como processado com sucesso e define o valor final
        """
        self.valor_enriquecido = valor_enriquecido
        self.sucess = True
        self.mensagem_erro = None
        self.processado_em = datetime. now()

    async def marcar_falha(self, mensagem_erro: str) -> None:
        """
        Achata o registro (origem + enriquecimento em um único dicionário
        pronto para ser transformado em linha de um DataFrame/Parquet de saída.)
        """

        base = self.registro_origem.to_dict()
        base.update({
            "valor_enriquecido": self.valor_enriquecido,
            "sucesso": self.sucess,
            "mensagem_erro": self.mensagem_erro,
            "processamento_em": self.processado_em.isoformat() if self.processado_em else None,
        })


        # Inclui os campos bruts extraídos da tela, prefixados para evitar colisão
        for nome_campo, valor in self.dados_tela.items():
            base[f'tela_{nome_campo}'] = valor

        return base