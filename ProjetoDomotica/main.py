from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ProjetoDomotica.database.database import engine, Base
from ProjetoDomotica.routers import comodos, dispositivos, cenas, acoes

app = FastAPI(title="Domótica – Pacote 1")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(comodos.router)
app.include_router(dispositivos.router)
app.include_router(acoes.router)
app.include_router(cenas.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
