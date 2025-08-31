from fastapi import FastAPI
from database import engine, Base
from routers import comodos, dispositivos, cenas, acoes

app = FastAPI(title="Domótica – Pacote 1")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(comodos.router)
app.include_router(dispositivos.router)
app.include_router(cenas.router)
app.include_router(acoes.router)

@app.get("/")
def home():
    return {"status": "ok", "msg": "API no ar"}
