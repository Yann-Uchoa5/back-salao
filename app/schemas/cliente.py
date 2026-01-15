from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255, description="Nome do cliente")
    data_procedimento: date = Field(..., description="Data do procedimento")
    tipo_procedimento: str = Field(..., min_length=1, max_length=100, description="Tipo do procedimento realizado")
    qtd_tonalizante: Optional[float] = Field(None, ge=0, description="Quantidade de tonalizante utilizado")
    valor_procedimento: float = Field(..., ge=0, description="Valor do procedimento")
    observacao: Optional[str] = Field(None, max_length=1000, description="Observações sobre o procedimento")
    corte: bool = Field(default=False, description="Indica se foi realizado corte")


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=255)
    data_procedimento: Optional[date] = None
    tipo_procedimento: Optional[str] = Field(None, min_length=1, max_length=100)
    qtd_tonalizante: Optional[float] = Field(None, ge=0)
    valor_procedimento: Optional[float] = Field(None, ge=0)
    observacao: Optional[str] = Field(None, max_length=1000)
    corte: Optional[bool] = None


class ClienteOut(ClienteBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

