from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=1, description="Senha")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UsuarioOut"


class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    nome_completo: Optional[str] = Field(None, max_length=255, description="Nome completo")


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6, description="Senha (mínimo 6 caracteres)")
    is_admin: bool = Field(default=False, description="Indica se o usuário é administrador")


class UsuarioOut(UsuarioBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Atualiza a referência forward
TokenResponse.model_rebuild()

