from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    tipo = Column(String, index=True, nullable=False)
    nivel = Column(Float, nullable=False)
    captura = Column(Float, nullable=False)
