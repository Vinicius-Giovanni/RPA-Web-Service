from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.config.settings import get_settings

class EmailTemplateRenderer:
    def __init__(self, template_dir: Path | None = None):
        directory = template_dir or get_settings().templates.email_dir
        self.environment = Environment(
            loader=FileSystemLoader(str(directory)),
            autoescape=select_autoescape(enabled_extensions=("html", "xml")),
        )

    def render(self, template_name: str, context: dict[str, Any]) -> str:
        template = self.environment.get_template(template_name)
        return template.render(**context)