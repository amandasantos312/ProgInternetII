from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ProjetoDomotica.database.database import get_db
from ProjetoDomotica.model.models import Acao, Dispositivo
from ProjetoDomotica.database.schemas import AcaoCreate, AcaoOut, AcaoUpdate
from typing import List, Optional


router = APIRouter(prefix="/acoes", tags=["Ações"])

@router.post("/", response_model=AcaoOut, status_code=status.HTTP_201_CREATED)
def criar_acao(payload: AcaoCreate, db: Session = Depends(get_db)):
    dispositivo = db.get(Dispositivo, payload.dispositivo_id)
    if not dispositivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo não encontrado.",
        )

    existente = (
        db.query(Acao)
        .filter(Acao.descricao.ilike(payload.descricao), Acao.dispositivo_id == payload.dispositivo_id)
        .first()
    )
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma ação com essa descrição para este dispositivo.",
        )

    acao = Acao(**payload.dict())
    db.add(acao)
    db.commit()
    db.refresh(acao)
    return acao

@router.get("/", response_model=List[AcaoOut])
def listar_acoes(
    dispositivo_id: Optional[int] = Query(None, description="Filtrar por dispositivo"),
    db: Session = Depends(get_db),
):
    query = db.query(Acao)
    if dispositivo_id:
        query = query.filter(Acao.dispositivo_id == dispositivo_id)
    return query.all()

@router.patch("/{acao_id}", response_model=AcaoOut)
def atualizar_acao(acao_id: int, payload: AcaoUpdate, db: Session = Depends(get_db)):
    acao = db.get(Acao, acao_id)
    if not acao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ação não encontrada.",
        )

    data = payload.dict(exclude_unset=True)

    if "descricao" in data:
        existente = (
            db.query(Acao)
            .filter(Acao.descricao.ilike(data["descricao"]), Acao.dispositivo_id == acao.dispositivo_id, Acao.id != acao.id)
            .first()
        )
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma ação com essa descrição para este dispositivo.",
            )
        acao.descricao = data["descricao"]

    if "dispositivo_id" in data:
        dispositivo = db.get(Dispositivo, data["dispositivo_id"])
        if not dispositivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dispositivo não encontrado.",
            )
        acao.dispositivo_id = data["dispositivo_id"]

    db.commit()
    db.refresh(acao)
    return acao

@router.delete("/{acao_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_acao(acao_id: int, db: Session = Depends(get_db)):
    acao = db.get(Acao, acao_id)
    if not acao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ação não encontrada.",
        )
    db.delete(acao)
    db.commit()
    return
