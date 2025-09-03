# routers/comodos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ProjetoDomotica.database.database import get_db
from ProjetoDomotica.model.models import Comodo
from ProjetoDomotica.database.schemas import ComodoCreate, ComodoOut


router = APIRouter(prefix="/comodos", tags=["Cômodos"])

@router.post("/", response_model=ComodoOut, status_code=status.HTTP_201_CREATED)
def criar_comodo(payload: ComodoCreate, db: Session = Depends(get_db)):
    existente = db.query(Comodo).filter(Comodo.nome.ilike(payload.nome)).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um cômodo com esse nome.",
        )
    c = Comodo(nome=payload.nome)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("/", response_model=list[ComodoOut])
def listar_comodos(db: Session = Depends(get_db)):
    return db.query(Comodo).all()

@router.put("/{comodo_id}", response_model=ComodoOut)
def atualizar_comodo(comodo_id: int, payload: ComodoCreate, db: Session = Depends(get_db)):
    c = db.get(Comodo, comodo_id)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cômodo não encontrado.",
        )

    existente = (
        db.query(Comodo)
        .filter(Comodo.nome.ilike(payload.nome), Comodo.id != comodo_id)
        .first()
    )
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um cômodo com esse nome.",
        )

    c.nome = payload.nome
    db.commit()
    db.refresh(c)
    return c

@router.delete("/{comodo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_comodo(comodo_id: int, db: Session = Depends(get_db)):
    c = db.get(Comodo, comodo_id)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cômodo não encontrado.",
        )

    if c.dispositivos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível remover um cômodo com dispositivos vinculados.",
        )

    db.delete(c)
    db.commit()
    return

@router.get("/{comodo_id}/vinculos")
def verificar_vinculos(comodo_id: int, db: Session = Depends(get_db)):
    c = db.get(Comodo, comodo_id)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cômodo não encontrado.",
        )

    return {
        "comodo": {"id": c.id, "nome": c.nome},
        "quantidade_dispositivos": len(c.dispositivos),
        "dispositivos": [
            {"id": d.id, "nome": d.nome, "tipo": d.tipo, "estado": d.estado}
            for d in c.dispositivos
        ],
    }
