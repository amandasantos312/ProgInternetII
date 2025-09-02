from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from ProjetoDomotica.database.database import Base


# Tabela de associação entre Comodo e Dispositivo
comodo_dispositivo = Table(
    "comodo_dispositivo",
    Base.metadata,
    Column("comodo_id", Integer, ForeignKey("comodos.id", ondelete="CASCADE"), primary_key=True),
    Column("dispositivo_id", Integer, ForeignKey("dispositivos.id", ondelete="CASCADE"), primary_key=True),
)

# Tabela de associação entre Cena e Acao
cena_acoes = Table(
    "cena_acoes",
    Base.metadata,
    Column("cena_id", Integer, ForeignKey("cenas.id", ondelete="CASCADE"), primary_key=True),
    Column("acao_id", Integer, ForeignKey("acoes.id", ondelete="CASCADE"), primary_key=True),
)

# Modelos (Classes)
class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    estado = Column(Boolean, nullable=False, default=False)
    
    # Relação com Comodo (Many-to-Many)
    comodos = relationship(
        "Comodo",
        secondary=comodo_dispositivo,
        back_populates="dispositivos",
        passive_deletes=True,
    )

class Comodo(Base):
    __tablename__ = "comodos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    
    # Relação com Dispositivo (Many-to-Many)
    dispositivos = relationship(
        "Dispositivo",
        secondary=comodo_dispositivo,
        back_populates="comodos",
        passive_deletes=True,
    )

class Acao(Base):
    __tablename__ = "acoes"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    dispositivo_id = Column(Integer, ForeignKey("dispositivos.id", ondelete="CASCADE"))

    # Relação com Dispositivo (Many-to-One)
    dispositivo = relationship("Dispositivo")
    
    # Relação com Cena (Many-to-Many)
    cenas = relationship(
        "Cena",
        secondary=cena_acoes,
        back_populates="acoes",
    )

class Cena(Base):
    __tablename__ = "cenas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    palavra_chave = Column(String, nullable=True)   # ← adiciona aqui
    estado = Column(String, default="inativa")

    # Relação com Acao (Many-to-Many)
    acoes = relationship(
        "Acao",
        secondary=cena_acoes,
        back_populates="cenas",
    )
