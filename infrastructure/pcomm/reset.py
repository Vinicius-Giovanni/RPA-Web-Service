from __future__ import annotations

from infrastructure.pcomm.client import PcommClient

class ResetPcomm:

    @staticmethod
    def reset_pcom(pcom = PcommClient) -> None:
            pcom.send_key('[pf9]')
            pcom.wait_ready()
            pcom.send_key('[pf3]')