from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class ProcedimentoBase(BaseModel):
    data_procedimento: date = Field(..., description="Data do procedimento")
    tipo_procedimento: str = Field(..., min_length=1, max_length=100, description="Tipo do procedimento realizado")
    qtd_tonalizante: Optional[float] = Field(None, ge=0, description="Quantidade de tonalizante utilizado")
    valor_procedimento: float = Field(..., ge=0, description="Valor do procedimento")
    observacao: Optional[str] = Field(None, max_length=1000, description="Observações sobre o procedimento")
    corte: bool = Field(default=False, description="Indica se foi realizado corte")


class ProcedimentoCreate(ProcedimentoBase):
    cliente_id: int = Field(..., description="ID do cliente")


class ProcedimentoUpdate(BaseModel):
    data_procedimento: Optional[date] = None
    tipo_procedimento: Optional[str] = Field(None, min_length=1, max_length=100)
    qtd_tonalizante: Optional[float] = Field(None, ge=0)
    valor_procedimento: Optional[float] = Field(None, ge=0)
    observacao: Optional[str] = Field(None, max_length=1000)
    corte: Optional[bool] = None


class ProcedimentoOut(ProcedimentoBase):
    id: int
    cliente_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

