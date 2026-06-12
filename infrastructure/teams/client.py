from __future__ import annotations

from typing import Any

import requests

from core.config.settings import get_settings
from core.logging.config import get_logger
from infrastructure.teams.template_renderer import TeamsTemplateRenderer

logger = get_logger(__name__)

class TeamsWebhookClient:
    def __init__(self, webhook_url: str | None = None, renderer: TeamsTemplateRenderer | None = None):
        self.webhook_url = webhook_url if webhook_url is not None else get_settings().inventory.teams_webhook
        self.renderer = renderer or TeamsTemplateRenderer()

    def send_card(self, template_name: str, context: dict[str, Any]) -> None:
        if not self.webhook_url:
            logger.warning("teams_webhook_not_configured")
            return
        
        payload = self.renderer.render(template_name, context)
        response = requests.post(self,self.webhook_url, json=payload, timeout=30)
        response.raise_for_status()
        logger.info("teams_card_sent", extra={"template": template_name})