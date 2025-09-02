from pydantic import BaseModel, Field
from typing import List, Optional


# --- Cômodo ---
class ComodoBase(BaseModel):
    nome: str

class ComodoCreate(ComodoBase):
    pass

class ComodoOut(ComodoBase):
    id: int
    class Config:
        orm_mode = True


# --- Dispositivo ---
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


# --- Ação ---
class AcaoBase(BaseModel):
    descricao: str
    dispositivo_id: int

class AcaoCreate(AcaoBase):
    pass

class AcaoOut(AcaoBase):
    id: int
    class Config:
        orm_mode = True

class AcaoUpdate(BaseModel):
    descricao: Optional[str] = None
    dispositivo_id: Optional[int] = None


# --- Cena ---
class CenaBase(BaseModel):
    nome: str
    palavra_chave: Optional[str] = Field(None, alias="palavra_chave")
    estado: Optional[str] = "inativa"

class CenaCreate(CenaBase):
    pass

class CenaOut(CenaBase):
    id: int
    acoes: List[AcaoOut] = []   # ← aqui aparecem as ações vinculadas
    class Config:
        orm_mode = True
