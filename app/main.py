from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import auth_routes
from app.routes import routes
from core.auth import auth_middleware

app = FastAPI()

# Mount the static files directory
app.mount('/static', StaticFiles(directory='frontend/static'), name='static')

# Set up templates
templates = Jinja2Templates(directory='frontend/templates')

app.middleware('http')(auth_middleware)
# include routers
app.include_router(routes.router)
app.include_router(auth_routes.router)