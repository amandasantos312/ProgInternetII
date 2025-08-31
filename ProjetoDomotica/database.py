from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#substitua os dados para que a conexão seja feita com o banco
DATABASE_URL = "postgresql+psycopg2://postgres:1112@localhost:5432/domotica"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()