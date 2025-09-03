from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ProjetoDomotica.database.database import get_db
from ProjetoDomotica.model.models import Cena, Acao
from ProjetoDomotica.database.schemas import CenaCreate, CenaOut, CenaUpdate
from typing import List, Optional


router = APIRouter(prefix="/cenas", tags=["Cenas"])

@router.post("/", response_model=CenaOut, status_code=status.HTTP_201_CREATED)
def criar_cena(payload: CenaCreate, db: Session = Depends(get_db)):
    existente = db.query(Cena).filter(Cena.nome.ilike(payload.nome)).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma cena com esse nome.",
        )

    cena = Cena(**payload.dict())
    db.add(cena)
    db.commit()
    db.refresh(cena)
    return cena

@router.get("/", response_model=List[CenaOut])
def listar_cenas(
    nome: Optional[str] = Query(None, description="Filtrar cenas pelo nome"),
    db: Session = Depends(get_db),
):
    query = db.query(Cena)
    if nome:
        query = query.filter(Cena.nome.ilike(f"%{nome}%"))
    return query.all()

@router.get("/{cena_id}", response_model=CenaOut)
def obter_cena(cena_id: int, db: Session = Depends(get_db)):
    cena = db.get(Cena, cena_id)
    if not cena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cena não encontrada.",
        )
    return cena

@router.patch("/{cena_id}", response_model=CenaOut)
def atualizar_cena(cena_id: int, payload: CenaUpdate, db: Session = Depends(get_db)):
    cena = db.get(Cena, cena_id)
    if not cena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cena não encontrada.",
        )

    data = payload.dict(exclude_unset=True)

    if "nome" in data:
        existente = (
            db.query(Cena)
            .filter(Cena.nome.ilike(data["nome"]), Cena.id != cena.id)
            .first()
        )
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma cena com esse nome.",
            )
        cena.nome = data["nome"]

    if "descricao" in data:
        cena.descricao = data["descricao"]

    db.commit()
    db.refresh(cena)
    return cena

@router.delete("/{cena_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_cena(cena_id: int, db: Session = Depends(get_db)):
    cena = db.get(Cena, cena_id)
    if not cena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cena não encontrada.",
        )
    db.delete(cena)
    db.commit()
    return

@router.post("/{cena_id}/acoes/{acao_id}", response_model=CenaOut)
def adicionar_acao_na_cena(cena_id: int, acao_id: int, db: Session = Depends(get_db)):
    cena = db.get(Cena, cena_id)
    if not cena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cena não encontrada.",
        )

    acao = db.get(Acao, acao_id)
    if not acao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ação não encontrada.",
        )

    if acao not in cena.acoes:
        cena.acoes.append(acao)
        db.commit()
        db.refresh(cena)

    return cena

@router.delete("/{cena_id}/acoes/{acao_id}", response_model=CenaOut)
def remover_acao_da_cena(cena_id: int, acao_id: int, db: Session = Depends(get_db)):
    cena = db.get(Cena, cena_id)
    if not cena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cena não encontrada.",
        )

    acao = db.get(Acao, acao_id)
    if not acao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ação não encontrada.",
        )

    if acao in cena.acoes:
        cena.acoes.remove(acao)
        db.commit()
        db.refresh(cena)

    return cena
