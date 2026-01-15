from sqlalchemy import Column, Integer, String, Date, Float, Boolean, DateTime
from sqlalchemy.sql import func
from db.base import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    data_procedimento = Column(Date, nullable=False)
    tipo_procedimento = Column(String, nullable=False)
    qtd_tonalizante = Column(Float, nullable=True)
    valor_procedimento = Column(Float, nullable=False)
    observacao = Column(String, nullable=True)
    corte = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

