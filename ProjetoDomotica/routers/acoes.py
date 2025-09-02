from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ProjetoDomotica.database.database import get_db
from ProjetoDomotica.model.models import Acao, Dispositivo
from ProjetoDomotica.database.schemas import AcaoCreate, AcaoOut, AcaoUpdate
from typing import List


router = APIRouter(prefix="/acoes", tags=["Ações"])

# Criar ação
@router.post("/", response_model=AcaoOut, status_code=201)
def criar_acao(payload: AcaoCreate, db: Session = Depends(get_db)):
    dispositivo = db.get(Dispositivo, payload.dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")

    acao = Acao(**payload.dict())
    db.add(acao)
    db.commit()
    db.refresh(acao)
    return acao

# Listar ações
@router.get("/", response_model=List[AcaoOut])
def listar_acoes(db: Session = Depends(get_db)):
    return db.query(Acao).all()

# Atualizar ação
@router.patch("/{acao_id}", response_model=AcaoOut)
def atualizar_acao(acao_id: int, payload: AcaoUpdate, db: Session = Depends(get_db)):
    acao = db.get(Acao, acao_id)
    if not acao:
        raise HTTPException(status_code=404, detail="Ação não encontrada")

    if payload.descricao is not None:
        acao.descricao = payload.descricao
    if payload.dispositivo_id is not None:
        dispositivo = db.get(Dispositivo, payload.dispositivo_id)
        if not dispositivo:
            raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
        acao.dispositivo_id = payload.dispositivo_id

    db.commit()
    db.refresh(acao)
    return acao

# Remover ação
@router.delete("/{acao_id}", status_code=204)
def remover_acao(acao_id: int, db: Session = Depends(get_db)):
    acao = db.get(Acao, acao_id)
    if not acao:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    db.delete(acao)
    db.commit()
