from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Associação N:N entre comodos e dispositivos
comodo_dispositivo = Table(
    "comodo_dispositivo",
    Base.metadata,
    Column("comodo_id", Integer, ForeignKey("comodos.id", ondelete="CASCADE"), primary_key=True),
    Column("dispositivo_id", Integer, ForeignKey("dispositivos.id", ondelete="CASCADE"), primary_key=True),
)

class Comodo(Base):
    __tablename__ = "comodos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)

    dispositivos = relationship(
        "Dispositivo",
        secondary=comodo_dispositivo,
        back_populates="comodos",
        passive_deletes=True,
    )

class Dispositivo(Base):
    __tablename__ = "dispositivos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    estado = Column(Boolean, nullable=False, default=False)

    comodos = relationship(
        "Comodo",
        secondary=comodo_dispositivo,
        back_populates="dispositivos",
        passive_deletes=True,
    )
