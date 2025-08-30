from pydantic import BaseModel
from typing import List, Optional

# ---------- Cômodo ----------
class ComodoBase(BaseModel):
    nome: str

class ComodoCreate(ComodoBase):
    pass

class ComodoOut(ComodoBase):
    id: int
    class Config:
        orm_mode = True

# ---------- Dispositivo ----------
class DispositivoBase(BaseModel):
    nome: str
    tipo: str
    estado: bool = False

class DispositivoCreate(DispositivoBase):
    comodo_ids: List[int] = []  # vincula 1..n cômodos ao criar

class DispositivoUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    estado: Optional[bool] = None

class DispositivoOut(DispositivoBase):
    id: int
    comodos: List[ComodoOut] = []
    class Config:
        orm_mode = True
