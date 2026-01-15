from sqlalchemy import Column, Integer, String, Date, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.base import Base


class Procedimento(Base):
    __tablename__ = "procedimentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False, index=True)
    data_procedimento = Column(Date, nullable=False, index=True)
    tipo_procedimento = Column(String, nullable=False)
    qtd_tonalizante = Column(Float, nullable=True)
    valor_procedimento = Column(Float, nullable=False)
    observacao = Column(String, nullable=True)
    corte = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento com Cliente
    cliente = relationship("Cliente", back_populates="procedimentos")

