from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from db.session import SessionLocal
from core.security import decode_access_token
from crud.auth import get_usuario_by_id
from models.usuario import Usuario

bearer_scheme = HTTPBearer(auto_error=False)


def get_db():
    """
    Dependency para obter uma sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependency para obter o usuário atual autenticado.
    """
    try:
        token = credentials.credentials
        payload = decode_access_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado. Faça login novamente.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        usuario_id = payload.get("id")
        if usuario_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: ID do usuário não encontrado no token.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        usuario = get_usuario_by_id(db, usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Usuário não encontrado no banco de dados (ID: {usuario_id}).",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not usuario.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo. Contate o administrador.",
            )
        
        return usuario
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Captura outros erros (como problemas de conexão com o banco)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Erro na autenticação: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_active_admin(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Dependency para verificar se o usuário atual é um administrador ativo.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores podem realizar esta ação."
        )
    return current_user

