from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ComodoBase(BaseModel):
    nome: str


class ComodoCreate(ComodoBase):
    pass


class ComodoUpdate(BaseModel):
    nome: Optional[str] = None


class ComodoOut(ComodoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DispositivoBase(BaseModel):
    nome: str
    tipo: str
    estado: bool = False


class DispositivoCreate(DispositivoBase):
    comodo_ids: List[int] = Field(default_factory=list)


class DispositivoUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    estado: Optional[bool] = None
    comodo_ids: Optional[List[int]] = None


class DispositivoOut(DispositivoBase):
    id: int
    comodos: List[ComodoOut] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class AcaoBase(BaseModel):
    descricao: str
    dispositivo_id: int


class AcaoCreate(AcaoBase):
    pass


class AcaoUpdate(BaseModel):
    descricao: Optional[str] = None
    dispositivo_id: Optional[int] = None



class CenaBase(BaseModel):
    nome: str
    palavra_chave: Optional[str] = None
    estado: Optional[str] = "inativa"


class CenaCreate(CenaBase):
    pass


class CenaUpdate(BaseModel):
    nome: Optional[str] = None
    palavra_chave: Optional[str] = None
    estado: Optional[str] = None


class CenaOut(CenaBase):
    id: int
    acoes: List[AcaoOut] = []
    class Config:
        orm_mode = True
