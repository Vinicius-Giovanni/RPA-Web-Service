from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv
from settings.paths import ENV_PATH

load_dotenv(dotenv_path=ENV_PATH)

DEPARTMENT_EMAIL = os.getenv('DEPARTMENT_EMAIL')
MANAGER_EMAIL = os.getenv('MANAGER_EMAIL')

BASE_DIR = Path(__file__).resolve().parent

@dataclass(frozen=True, slot=True)
class SupabaseSettings:
    url: str = ''
    anon_key: str = ''
    jwt_secret: str = ''
    jwks_url: str = "/auth/v1/.well-known/jwks.json"

    @property
    def is_configured(self) -> bool:
        return bool(self.url and self.anon_key)
    
@dataclass(frozen=True, slots=True)
class SecuritySettings:
    access_token_cookie: str = "access_token"
    jwt_algorithms: tuple[str, ...] = ("ES256",)
    secure_cookies: bool = False
    same_site: str = "lax"

@dataclass(frozen=True, slots=True)
class LoggingSettings:
    log_dir: Path = BASE_DIR / "logs"
    execution_dir: Path = BASE_DIR / "logs" / "executions"
    error_dir: Path = BASE_DIR / 'logs' / 'audit'
    max_bytes: int = 10 * 1024 * 1024
    backup_count: int = 10
    level: str = "INFO"


@dataclass(frozen=True, slots=True)
class TemplateSettings:
    frontend_dir: Path = BASE_DIR / "frontend" / "templates"
    static_dir: Path = BASE_DIR / "frontend" / "static"
    email_dir: Path = BASE_DIR / "templates" / "emails"
    teams_dir: Path = BASE_DIR / "templates" / "teams"

@dataclass(frozen=True, slots=True)
class InventoryAutomationSettings:
    schedule_disparo: tuple[str, ...] = ("08:55", "15:55", "20:55", "02:55")
    test_mode: bool = False
    department_email: str = DEPARTMENT_EMAIL
    manager_emails: tuple[str, ...] = (MANAGER_EMAIL)
    teams_webhook: str = ""
    teams_header_message: str = (
        "🚨 **ILPNs sem local, que ainda temos pendências em atraso crítico.**\n\n"
        "Peço, por favor, que verifiquem com o time e avancem nas tratativas das que ainda estão abertas. "
        "**Obrigado pelo apoio de todos!**"
    )

@dataclass(frozen=True, slots=True)
class AppSettings:
    app_name: str = "Web RPA Service - WaveHub"
    Environment: str = "local"
    debug: bool = False
    base_dir: Path = BASE_DIR
    supabase: SupabaseSettings = field(default_factory=SupabaseSettings)
    security: SecuritySettings = field(default_factory=SecuritySettings)
    logging: LoggingSettings = field(default_factory=LoggingSettings)
    templates: TemplateSettings = field(default_factory=TemplateSettings)
    inventory: InventoryAutomationSettings = field(default_factory=InventoryAutomationSettings)

def _bool_env(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {'1', 'true', 'yes', 'on'}

def _tuple_env(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    raw = os.getenv(name)
    if not raw:
        return default
    return tuple(item.strip() for item in raw.split(',') if item.strip())

@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings(
        app_name=os.getenv("APP_NAME"),
        environment=os.getenv("APP_ENV"),
        debug=_bool_env("APP_DEBUG"),
        supabase=SupabaseSettings(
            url=os.getenv("API_URL"),
            anon_key=os.getenv("API_KEY_ANON_PUBLIC"),
            jwt_secret=os.getenv("JWT_SECRET"),
            jwks_url=os.getenv("JWKS_URL"),
        ),
        security=SecuritySettings(secure_cookies=_bool_env("SECURE_COOKIES")),
        inventory=InventoryAutomationSettings(
            test_mode=_bool_env("MODO_TESTE"),
            department_email=os.getenv("DEPARTMENT_EMAIL"),
            manager_emails=_tuple_env("EMAILS_GESTORES"),
            teams_webhook = os.getenv("WEBHOOK_TEAMS"),
        ),
    )