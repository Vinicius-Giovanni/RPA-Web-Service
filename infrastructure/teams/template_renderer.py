from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from core.config.settings import get_settings

class TeamsTemplateRenderer:
    def __init__(self, template_dir: Path | None = None):
        directory = template_dir or get_settings().templates.teams_dir
        self.environment  = Environment(loader=FileSystemLoader(str(directory)), autoescape=False)

    def render(self, template_name: str, context: dict[str, Any]) -> dict[str, Any]:
        payload = self.environment.get_template(template_name).render(**context)
        return dict(json.loads(payload))