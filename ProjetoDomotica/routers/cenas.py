from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cena, Acao
from schemas import CenaCreate, CenaOut
from typing import List

router = APIRouter(prefix="/cenas", tags=["Cenas"])

# Criar cena
@router.post("/", response_model=CenaOut, status_code=201)
def criar_cena(payload: CenaCreate, db: Session = Depends(get_db)):
    cena = Cena(**payload.dict())
    db.add(cena)
    db.commit()
    db.refresh(cena)
    return cena

# Listar cenas (com ações vinculadas)
@router.get("/", response_model=List[CenaOut])
def listar_cenas(db: Session = Depends(get_db)):
    return db.query(Cena).all()

# Obter cena específica
@router.get("/{cena_id}", response_model=CenaOut)
def obter_cena(cena_id: int, db: Session = Depends(get_db)):
    cena = db.get(Cena, cena_id)
    if not cena:
        raise HTTPException(status_code=404, detail="Cena não encontrada")
    return cena

# Excluir cena
@router.delete("/{cena_id}", status_code=204)
def remover_cena(cena_id: int, db: Session = Depends(get_db)):
    cena = db.get(Cena, cena_id)
    if not cena:
        raise HTTPException(status_code=404, detail="Cena não encontrada")
    db.delete(cena)
    db.commit()

# --- Vínculos com ações ---

# Adicionar ação em uma cena
@router.post("/{cena_id}/acoes/{acao_id}", response_model=CenaOut)
def adicionar_acao_na_cena(cena_id: int, acao_id: int, db: Session = Depends(get_db)):
    cena = db.get(Cena, cena_id)
    if not cena:
        raise HTTPException(status_code=404, detail="Cena não encontrada")

    acao = db.get(Acao, acao_id)
    if not acao:
        raise HTTPException(status_code=404, detail="Ação não encontrada")

    if acao not in cena.acoes:
        cena.acoes.append(acao)
        db.commit()
        db.refresh(cena)

    return cena

# Remover ação de uma cena
@router.delete("/{cena_id}/acoes/{acao_id}", response_model=CenaOut)
def remover_acao_da_cena(cena_id: int, acao_id: int, db: Session = Depends(get_db)):
    cena = db.get(Cena, cena_id)
    if not cena:
        raise HTTPException(status_code=404, detail="Cena não encontrada")

    acao = db.get(Acao, acao_id)
    if not acao:
        raise HTTPException(status_code=404, detail="Ação não encontrada")

    if acao in cena.acoes:
        cena.acoes.remove(acao)
        db.commit()
        db.refresh(cena)

    return cena
