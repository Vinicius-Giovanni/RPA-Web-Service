from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes.routes import router
app = FastAPI()

# Mount the static files directory
app.mount('/static', StaticFiles(directory='frontend/static'), name='static')

# Set up templates
templates = Jinja2Templates(directory='frontend/templates')

# include routers
app.include_router(router)