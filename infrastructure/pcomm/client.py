from __future__ import annotations

from typing import Optional

import pythoncom
import win32com.client

class PcommClient:

    def __init__(self):
        self.conn_list = None
        self.session = None
        self.ps = None
        self.oia = None

    def connect(self):
        pythoncom.CoInitialize()

        self.conn_list = win32com.client.Dispatch(
            "PCOMM.autECLConnList"
        )

        self.conn_list.Refresh()

        if self.conn_list.Count == 0:
            raise RuntimeError(
                "Nenhuma sessão PCOMM aberta encontrada"
            )

        target = self.conn_list.ConnInfo(1)

        print('Usando sessão:')
        print('Nome:', target.Name)
        print('Handle:', target.Handle)

        self.session = win32com.client.Dispatch(
            "PCOMM.autECLSession"
        )

        self.session.SetConnectionByHandle(
            target.Handle
        )

        self.ps = self.session.autECLPS
        self.oia = self.session.autECLOIA


    def disconnect(self):
        self.ps = None
        self.oia = None
        self.session = None
        self.conn_list = None

        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

    def send_text(
            self,
            text: str,
            row: Optional[int] = None,
            column: Optional[int] = None
    ):
        if row is not None and column is not None:
            self.ps.SetCursorPos(row, column)

        self.ps.SendKeys(text)

    def send_key(self, key: str):
        """
        Exemplos:

        send_key('[enter]')
        send_key('[pf3]')
        send_key('[clear]')
        send_key('[pf12]')
        """

        self.ps.SendKeys(key)
    
    def read(
            self,
            row: int,
            column: int,
            length: int
    ) -> str:
        
        return self.ps.GetText(
            row,
            column,
            length
        ).strip()
    
    def wait_text(
            self,
            row: int,
            column: int,
            length: int,
            timeout: int = 0.1,
            default: str = 'VAZIO'
    ):
        import time

        start = time.time()

        while True:

            value = self.read(
                row=row,
                column=column,
                length=length
            )

            if value.strip():
                return value.strip()
            
            if time.time() - start > timeout:
                return default
            
            time.sleep(0.2)

    def wait_ready(self, timeout: int = 30):

        import time

        start = time.time()

        while True:

            if self.oia.InputInhibited == 0:
                return

            if time.time() - start > timeout:
                raise TimeoutError(
                    "Terminal não ficou disponível."
                )

            time.sleep(0.1)

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_Val, exc_tb):
        self.disconnect()