from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from model import Base

class Treino(Base):
    __tablename__ = "treino"

    id= Column("pk_treino", Integer, primary_key=True)
    nome= Column(String(140), unique=True)
    quantidade = Column(Integer)

    def __init__(self, nome, quantidade):
        self.nome = nome
        self.quantidade = quantidade
