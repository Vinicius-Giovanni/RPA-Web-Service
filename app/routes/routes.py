from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import uvicorn

routes = FastAPI()

# TEMPLATES
templates = Jinja2Templates(directory='frontend/templates')

# STATIC
routes.mount('/static', StaticFiles(directory='frontend/static'), name='static')

@routes.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={}
    )

@routes.get('/login', response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='login.html',
        context={}
    )

@routes.get('/cadastro', response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='register.html',
        context={}
    )