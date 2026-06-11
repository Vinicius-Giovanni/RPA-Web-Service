from __future__ import annotations

from collections.abc import Sequence

from core.config.settings import get_settings
from core.logging.config import get_audit_logger
from infrastructure.email.template_renderer import EmailTemplateRenderer

logger = get_audit_logger()

class OutlookEmailSender:
    def __init__(self, renderer: EmailTemplateRenderer | None = None, test_mode: bool | None = None):
        self.renderer = renderer or EmailTemplateRenderer()
        self.test_mode = get_settings().inventory.test_mode if test_mode is None else test_mode
        self._outlook = None

    @property
    def outlook(self): # type: ignore[no-untyped-def]
        if self._outlook is None:
            import win32com.client as win32

            self._outlook = win32.Dispatch("outlook.application")
        return self._outlook
    
    def send_template(
            self,
            subject: str,
            to: Sequence[str],
            cc: Sequence[str],
            template_name: str,
            context: dict[str, object],
    ) -> bool:
        message = self.outlook.CreateItem(0)
        message.To = ";".join(to)
        message.CC = ";".join(cc)
        message.Subject = subject
        message.HTMLBody = self.renderer.render(template_name, context)
        if not message.Recipients.ResolveAll():
            logger.error("invalid_email_recipent", extra={"to": message.To})
            return False
        if self.test_mode:
            message.Save()
        else:
            message.Send()
        logger.info("email_sent", extra={"subject": subject, "test_mode": self.test_mode})
        return True