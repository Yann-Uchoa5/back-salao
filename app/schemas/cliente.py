from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255, description="Nome do cliente")


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=255)


class ClienteOut(ClienteBase):
    id: int
    caminho_foto: Optional[str] = Field(None, description="Caminho para a foto do cliente")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ClienteComProcedimentosOut(ClienteOut):
    """
    Cliente com lista de procedimentos (histórico completo).
    """
    procedimentos: List["ProcedimentoOut"] = Field(default_factory=list, description="Histórico de procedimentos do cliente")


# Resolve referências forward após importar ProcedimentoOut
from schemas.procedimento import ProcedimentoOut
ClienteComProcedimentosOut.model_rebuild()

