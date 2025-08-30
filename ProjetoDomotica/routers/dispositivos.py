# routers/dispositivos.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Dispositivo, Comodo
from schemas import DispositivoCreate, DispositivoOut, DispositivoUpdate

router = APIRouter(prefix="/dispositivos", tags=["Dispositivos"])

@router.post("/", response_model=DispositivoOut, status_code=201)
def criar_dispositivo(payload: DispositivoCreate, db: Session = Depends(get_db)):
    d = Dispositivo(nome=payload.nome, tipo=payload.tipo, estado=payload.estado)

    if payload.comodo_ids:
        ids_unicos = list(set(payload.comodo_ids))
        comodos = db.query(Comodo).filter(Comodo.id.in_(ids_unicos)).all()
        if len(comodos) != len(ids_unicos):
            raise HTTPException(status_code=400, detail="Um ou mais cômodos não existem.")
        d.comodos = comodos

    db.add(d)
    db.commit()
    db.refresh(d)
    return d


@router.get("/", response_model=list[DispositivoOut])
def listar_dispositivos(
    incluir_comodos: bool = Query(True, description="Se true, retorna os cômodos vinculados"),
    db: Session = Depends(get_db),
):
    itens = db.query(Dispositivo).all()
    # o Pydantic com orm_mode já serializa com comodos; a flag existe só se quiser
    if incluir_comodos:
        return itens
    # sem comodos: mapeia resposta manual
    return [
        {"id": i.id, "nome": i.nome, "tipo": i.tipo, "estado": i.estado, "comodos": []}
        for i in itens
    ]

@router.get("/{dispositivo_id}", response_model=DispositivoOut)
def obter_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    d = db.get(Dispositivo, dispositivo_id)
    if not d:
        raise HTTPException(404, "Dispositivo não encontrado.")
    return d

@router.patch("/{dispositivo_id}", response_model=DispositivoOut)
def atualizar_dispositivo(dispositivo_id: int, payload: DispositivoUpdate, db: Session = Depends(get_db)):
    d = db.get(Dispositivo, dispositivo_id)
    if not d:
        raise HTTPException(404, "Dispositivo não encontrado.")
    data = payload.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(d, k, v)
    db.commit()
    db.refresh(d)
    return d

@router.delete("/{dispositivo_id}", status_code=204)
def remover_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    d = db.get(Dispositivo, dispositivo_id)
    if not d:
        raise HTTPException(404, "Dispositivo não encontrado.")
    db.delete(d)
    db.commit()
    return

# Vincular dispositivo a um cômodo
@router.post("/{dispositivo_id}/comodos/{comodo_id}", status_code=204)
def vincular(dispositivo_id: int, comodo_id: int, db: Session = Depends(get_db)):
    d = db.get(Dispositivo, dispositivo_id)
    c = db.get(Comodo, comodo_id)
    if not d or not c:
        raise HTTPException(404, "Dispositivo ou cômodo não encontrado.")
    if c not in d.comodos:
        d.comodos.append(c)
        db.commit()
    return

# Desvincular
@router.delete("/{dispositivo_id}/comodos/{comodo_id}", status_code=204)
def desvincular(dispositivo_id: int, comodo_id: int, db: Session = Depends(get_db)):
    d = db.get(Dispositivo, dispositivo_id)
    c = db.get(Comodo, comodo_id)
    if not d or not c:
        raise HTTPException(404, "Dispositivo ou cômodo não encontrado.")
    if c in d.comodos:
        d.comodos.remove(c)
        db.commit()
    return
