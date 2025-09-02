# routers/comodos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ProjetoDomotica.database.database import get_db
from ProjetoDomotica.model.models import Comodo
from ProjetoDomotica.database.schemas import ComodoCreate, ComodoOut


router = APIRouter(prefix="/comodos", tags=["Cômodos"])

@router.post("/", response_model=ComodoOut, status_code=201)
def criar_comodo(payload: ComodoCreate, db: Session = Depends(get_db)):
    existente = db.query(Comodo).filter(Comodo.nome == payload.nome).first()
    if existente:
        raise HTTPException(400, "Já existe um cômodo com esse nome.")
    c = Comodo(nome=payload.nome)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("/", response_model=list[ComodoOut])
def listar_comodos(db: Session = Depends(get_db)):
    return db.query(Comodo).all()

@router.delete("/{comodo_id}", status_code=204)
def remover_comodo(comodo_id: int, db: Session = Depends(get_db)):
    c = db.get(Comodo, comodo_id)
    if not c:
        raise HTTPException(404, "Cômodo não encontrado.")
    db.delete(c)
    db.commit()
    return

# Verificar vínculos: dispositivos do cômodo
@router.get("/{comodo_id}/vinculos")
def verificar_vinculos(comodo_id: int, db: Session = Depends(get_db)):
    c = db.get(Comodo, comodo_id)
    if not c:
        raise HTTPException(404, "Cômodo não encontrado.")
    return {
        "comodo": {"id": c.id, "nome": c.nome},
        "dispositivos": [{"id": d.id, "nome": d.nome, "tipo": d.tipo, "estado": d.estado} for d in c.dispositivos],
    }
