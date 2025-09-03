from fastapi import APIRouter, Depends, HTTPException, Query, Form, status
from sqlalchemy.orm import Session
from ProjetoDomotica.database.database import get_db
from ProjetoDomotica.model.models import Dispositivo, Comodo
from ProjetoDomotica.database.schemas import DispositivoCreate, DispositivoOut, DispositivoUpdate


router = APIRouter(prefix="/dispositivos", tags=["Dispositivos"])

@router.post("/", response_model=DispositivoOut, status_code=status.HTTP_201_CREATED)
def criar_dispositivo(payload: DispositivoCreate, db: Session = Depends(get_db)):
    existente = db.query(Dispositivo).filter(Dispositivo.nome.ilike(payload.nome)).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um dispositivo com esse nome.",
        )

    d = Dispositivo(nome=payload.nome, tipo=payload.tipo, estado=payload.estado)
    db.add(d)

    if payload.comodo_ids:
        ids_unicos = list(set(payload.comodo_ids))
        comodos = db.query(Comodo).filter(Comodo.id.in_(ids_unicos)).all()

        if len(comodos) != len(ids_unicos):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Um ou mais cômodos não existem.",
            )

        d.comodos.extend(comodos)

    db.commit()
    db.refresh(d)
    return d

@router.get("/", response_model=list[DispositivoOut])
def listar_dispositivos(
    incluir_comodos: bool = Query(True, description="Se true, retorna os cômodos vinculados"),
    db: Session = Depends(get_db),
):
    itens = db.query(Dispositivo).all()

    if incluir_comodos:
        return itens

    return [
        {"id": i.id, "nome": i.nome, "tipo": i.tipo, "estado": i.estado, "comodos": []}
        for i in itens
    ]

@router.get("/{dispositivo_id}", response_model=DispositivoOut)
def obter_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    d = db.get(Dispositivo, dispositivo_id)
    if not d:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo não encontrado.",
        )
    return d

@router.patch("/{dispositivo_id}", response_model=DispositivoOut)
def atualizar_dispositivo(dispositivo_id: int, payload: DispositivoUpdate, db: Session = Depends(get_db)):
    d = db.get(Dispositivo, dispositivo_id)
    if not d:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo não encontrado.",
        )

    data = payload.dict(exclude={"comodo_ids"}, exclude_unset=True)
    for k, v in data.items():
        setattr(d, k, v)

    if payload.comodo_ids is not None:
        ids_unicos = list(set(payload.comodo_ids))
        novos_comodos = db.query(Comodo).filter(Comodo.id.in_(ids_unicos)).all()

        if len(novos_comodos) != len(ids_unicos):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Um ou mais cômodos não existem.",
            )

        d.comodos = novos_comodos

    db.commit()
    db.refresh(d)
    return d

@router.delete("/{dispositivo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    d = db.get(Dispositivo, dispositivo_id)
    if not d:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo não encontrado.",
        )
    db.delete(d)
    db.commit()
    return

@router.post("/{dispositivo_id}/comodos/{comodo_id}", status_code=status.HTTP_204_NO_CONTENT)
def vincular(dispositivo_id: int, comodo_id: int, db: Session = Depends(get_db)):
    d = db.get(Dispositivo, dispositivo_id)
    c = db.get(Comodo, comodo_id)

    if not d or not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo ou cômodo não encontrado.",
        )

    if c not in d.comodos:
        d.comodos.append(c)
        db.commit()
    return

@router.delete("/{dispositivo_id}/comodos/{comodo_id}", status_code=status.HTTP_204_NO_CONTENT)
def desvincular(dispositivo_id: int, comodo_id: int, db: Session = Depends(get_db)):
    d = db.get(Dispositivo, dispositivo_id)
    c = db.get(Comodo, comodo_id)

    if not d or not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo ou cômodo não encontrado.",
        )

    if c in d.comodos:
        d.comodos.remove(c)
        db.commit()
    return
