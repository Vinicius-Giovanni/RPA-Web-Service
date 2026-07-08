from __future__ import annotations

import numpy as np
import pandas as pd

class DeadlineService:
    """
    Responsável pela classificação de prazo das oLPNs.
    """

    @staticmethod
    async def classify(df: pd.DataFrame) -> pd.DataFrame:

        required = {
            "status_olpn",
            "box",
            "data_locacao_pedido",
            "data_hora_ultimo_update_olpn",
        }

        if not required.issubset(df.columns):
            return df
        
        deadline_1 = (
            df['data_locacao_pedido'] + pd.Timedelta(days=1)
        ).dt.normalize() + pd.Timedelta(hours=5, minutes=30)

        deadline_2 = (
            df['data_locacao_pedido'] + pd.Timedelta(days=1)
        ).dt.normalize() + pd.Timedelta(hours=10)

        deadline_3 = (
            df['data_locacao_pedido']
        ).dt.normalize() + pd.Timedelta(hours=23, minutes=30)

        deadline_4 = (
            df['data_locacao_pedido'] + pd.Timedelta(days=1)
        ).dt.normalize() + pd.Timedelta(hours=18)

        shipped = (
            df['status_olpn'].eq('Shipped')
            & df['data_locacao_pedido'].notna()
        )

        result = pd.Series(
            pd.NA,
            index=df.index,
            dtypes='string',
        )

        rules = [
            (
                df['box'].between(413, 526),
                deadline_1,
            ),
            (
                df['box'].between(527, 556),
                deadline_2,
            ),
            (
                df['box'].between(331, 412),
                deadline_3,
            ),
            (
                df['box'].between(557, 584),
                deadline_4
            ),
        ]

        for mask, deadline in rules:

            current = shipped & mask

            result.loc[current] = np.where(
                df.loc[current, 'data_hora_ultimo_update_olpn']
                <= deadline.loc[current],
                "No prazo",
                "Fora do prazo",
            )

        df['situacao_prazo'] = result

        return df