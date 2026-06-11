from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.middlewares.observability import ObservabilityMiddleware
from api.routes import auth, pages
from core.config.settings import get_settings
from core.exceptions.handlers import register_exception_hadlers
from core.logging.config import configure_logging


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()

    app = FastAPI(title=settings.app_name, debug=settings.debug)
    app.mount("/static", StaticFiles(directory=str(settings.templates.static_dir)), name="static")
    app.add_middleware(ObservabilityMiddleware)
    register_exception_hadlers(app)
    app.include_router(pages.router)
    app.include_router(auth.router)

    return app

app = create_app()