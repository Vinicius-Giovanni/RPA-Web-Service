from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv
from settings.paths import ENV_PATH, BASE_DIR

"""
Centraliza as configurações da aplicação.

Este módulo é responsável por:

- Carregar variáveis de ambiente.
- Definir configurações tipadas através de dataclasses.
- Organizar parâmetros por domínio de responsabilidade.
- Disponibilizar uma instância única das configurações.

As configurações são carregadas a partir do arquivo '.env'
e disponibilizadas através da função 'get_settings".
"""

load_dotenv(dotenv_path=ENV_PATH)

DEPARTMENT_EMAIL = os.getenv('DEPARTMENT_EMAIL')
MANAGER_EMAIL = os.getenv('MANAGER_EMAIL')

@dataclass(frozen=True, slots=True)
class SupabaseSettings:
    """
    Configurações de integração com o Supabase.

    Attributes:
        url:
            URL base da instância Supabase.

        anon_key:
            Chave pública utilizada para autenticação da aplicação.

        jwt_secret:
            Chave secreta utilizada para validação de tokens JWT.

        jwks_url:
            Endpoint responsável por disponibilizar as chaves
            públicas utilizadas na validação dos tokens.
    """
    url: str = ''
    anon_key: str = ''
    jwt_secret: str = ''
    jwks_url: str = "/auth/v1/.well-known/jwks.json"

    @property
    def is_configured(self) -> bool:
        """
        Verifica se a integração com o Supabase foi configurada.

        Returns:
            bool:
                True quando URL e chave pública estão disponiveis.
        """
        return bool(self.url and self.anon_key)
    
@dataclass(frozen=True, slots=True)
class SecuritySettings:
    """
    Configurações relacionadas à autenticação e segurança.

    Attributes:
        access_token_cookie:
            Nome do cookie utilizado para armazenar o token JWT.

        jwt_algorithms:
            Algoritmos aceitos para validação dos tokens.
        
        secure_cookies:
            Define se os cookies devem ser enviados apenas
            através de conexões HTTS.
        
        same_site:
            Política SameSite aplicada aos cookies.
    """
    access_token_cookie: str = "access_token"
    jwt_algorithms: tuple[str, ...] = ("ES256",)
    secure_cookies: bool = False
    same_site: str = "lax"

@dataclass(frozen=True, slots=True)
class LoggingSettings:
    """
    Configurações do sistema de logging.

    Attributes:
        log_dir:
            Diretório principal dos logs.
        
        execution_dir:
            Diretório destinado aos logs de execução.
        
        error_dir:
            Diretório destinado aos logs de auditoria
            e erros.
        
        max_bytes:
            Tamanho máximo permitido para cada arquivo
            antes da rotação.

        backup_count:
            Quantidade máxima de backups mantidos.

        level:
            Nível padrão ed logging.
    """
    log_dir: Path = BASE_DIR / "logs"
    execution_dir: Path = BASE_DIR / "logs" / "executions"
    error_dir: Path = BASE_DIR / 'logs' / 'errors'
    audit_dir: Path = BASE_DIR / 'logs' / 'audit'

    max_bytes: int = 10 * 1024 * 1024
    backup_count: int = 10
    level: str = "INFO"


@dataclass(frozen=True, slots=True)
class TemplateSettings:
    """
    Configurações relacionadas aos templates da aplicação.

    Attributes:
        frontend_dir:
            Diretório dos templates HTML.

        static_dir:
            Diretório dos arquivos estáticos.

        email_dir:
            Diretório dos templates de e-mail.

        teams_dir:
            Diretório dos templates utilizados em integrações
            com Microsoft Teams.
    """
    frontend_dir: Path = BASE_DIR / "frontend" / "templates"
    static_dir: Path = BASE_DIR / "frontend" / "static"
    email_dir: Path = BASE_DIR / "frontend" /  "templates" / "emails"
    teams_dir: Path = BASE_DIR / "frontend" / "templates" / "teams"

@dataclass(frozen=True, slots=True)
class InventoryAutomationSettings:
    """
    Configurações da automação de inventário.

    Attributes:
        schedule_disparo:
            Horários programados para execução da automação.

        teste_mode:
            Indica se a automação está executando em modo teste.

        department_email:
            E-mail principal do departamento.

        manager_emails:
            Lista de e-mails dos gestores responsáveis.

        teams_webhook:
            URL do wehbhook utilizado para envio de notificações.

        teams_header_message:
            Mensagem paadrão utilizada nos alertas enviados.
        
    """
    schedule_disparo: tuple[str, ...] = ("08:55", "15:55", "20:55", "02:55")
    test_mode: bool = False
    department_email: str = DEPARTMENT_EMAIL
    manager_emails: tuple[str, ...] = (MANAGER_EMAIL,)
    teams_webhook: str = ""
    teams_header_message: str = (
        "🚨 **ILPNs sem local, que ainda temos pendências em atraso crítico.**\n\n"
        "Peço, por favor, que verifiquem com o time e avancem nas tratativas das que ainda estão abertas. "
        "**Obrigado pelo apoio de todos!**"
    )

@dataclass(frozen=True, slots=True)
class AppSettings:
    """
    Agrega todas as configurações da aplicação.

    Esta classe funciona como ponto central de acesso às
    configurações carregadas do ambiente.

    Attributes:
        app_name:
            Nome da aplicação.

        environment:
            Ambiente atual de execução.

        debug:
            Indica se o modo debug está habilitado.

        base_dir:
            Diretório raiz da aplicação.
        
        supabase:
            Configurações do Supabase.
        
        security:
            Configurações de segurança.

        logging:
            Configurações de logging.
        
        templates:
            Configurações dos templates.

        inventory:
            Configurações da automação de inventário.
    """
    app_name: str = "Web RPA Service - WaveHub"
    environment: str = "local"
    debug: bool = False
    base_dir: Path = BASE_DIR
    supabase: SupabaseSettings = field(default_factory=SupabaseSettings)
    security: SecuritySettings = field(default_factory=SecuritySettings)
    logging: LoggingSettings = field(default_factory=LoggingSettings)
    templates: TemplateSettings = field(default_factory=TemplateSettings)
    inventory: InventoryAutomationSettings = field(default_factory=InventoryAutomationSettings)

def _bool_env(name: str, default: bool = False) -> bool:
    """
    Converte uma variável de ambiente para booleano

    Valores aceitos como verdadeiros:
    - 1
    - true
    - yes
    - on

    Args:
        name:
            Nome da variável de ambiente.
        
        default:
            Valor retornado caso a variávelnão exista.
        
    Returns:
        bool:
            Valor convertido.
    """
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {'1', 'true', 'yes', 'on'}

def _tuple_env(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    """
    Converte uma variável de ambiente separada por vírgulas
    em uma tupla de strings.

    Exemplo:
        EMAILS=user1@email.com,user2@email.com

    Resultado:
        (
            "user1@email.com",
            "user2@email.com",
        )

    Args:
        name:
            Nome da variável de ambiente.

        default:
            Valor padrão caso a variável não exista.
    
    Returns:
        tuple[str, ...]:
            Tupla contendo os valores processados.
    """
    raw = os.getenv(name)
    if not raw:
        return default
    return tuple(item.strip() for item in raw.split(',') if item.strip())

@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """
    Retorna uma instância única das configurações da aplicação.

    As configurações são carregadas a partir das variáveis
    de ambiente e armazenadas em cache durante todo o ciclo
    de vida da aplicação.

    O uso de cache evita múltiplas leituras do ambiente e garante consistência dos valores utilizados.

    Returns:
        AppSettings:
            Objeto contendo todas as configurações carregadas.
    """
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
            manager_emails=_tuple_env("EMAILS_GESTORES", ()),
            teams_webhook = os.getenv("WEBHOOK_TEAMS"),
        ),
    )