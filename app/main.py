from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.middlewares.observability import ObservabilityMiddleware
from api.routes import auth, pages
from core.config.settings import get_settings
from core.exceptions.handlers import register_exception_handlers
from core.logging.config import configure_logging

"""
Ponto de entrada da aplicação.

Este módulo é responsável pela inicialização e configuração da
aplicação FastAPI, realizando a composição dos componentes
necessários para execução do sistema.

Configurações realizadas:

- Inicialização do FastAPI.
- Configuração do sistema de logging.
- Registro de middlewares.
- Registro de handlers globais de exceção.
- Configuração de arquivos estáticos.
- Registro das rotas da aplicação.

Estearquivo atua como Composition Root da arquitetura,
centralizando a integração entre as diferentes camadas
do sistema.
"""

def create_app() -> FastAPI:
    """
    Cria e configura uma instância da aplicação FastAPI.

    Durante a inicialização são executadas as seguintes etapas:

    1. Carregamento das configurações da aplicação.
    2. Configuração do sistema de logging.
    3. Criação da instância FastAPI.
    4. Registro dos arquivo estáticos.
    5. Configuração dos middlewares.
    6. Registro dos handlers globais de exceção.
    7. Inclusão das rotas da aplicação.

    Returns:
        FastAPI:
            Aplicação completamente configurada e pronta
            para execução.
    """
    settings = get_settings()
    configure_logging()

    app = FastAPI(title=settings.app_name, debug=settings.debug)
    app.mount("/static", StaticFiles(directory=str(settings.templates.static_dir)), name="static")
    app.add_middleware(ObservabilityMiddleware)
    register_exception_handlers(app)
    app.include_router(pages.router)
    app.include_router(auth.router)

    return app

# Instância principal utilizada pelo servidor ASGI.
app = create_app()