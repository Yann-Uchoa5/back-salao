from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from schemas.login import LoginRequest, TokenResponse, UsuarioCreate, UsuarioOut
from crud.auth import autenticar_usuario, criar_usuario
from core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from core.dependencies import get_db, get_current_user
from models.usuario import Usuario

router = APIRouter()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint de login. Aceita username e password.
    Retorna um token JWT e informações do usuário.
    """
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Cria o token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.username, "id": usuario.id, "role": "admin" if usuario.is_admin else "user"},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UsuarioOut.model_validate(usuario)
    }


@router.post("/login/json", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login alternativo que aceita JSON ao invés de form-data.
    Retorna um token JWT e informações do usuário.
    """
    usuario = autenticar_usuario(db, login_data.username, login_data.password)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Cria o token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.username, "id": usuario.id, "role": "admin" if usuario.is_admin else "user"},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UsuarioOut.model_validate(usuario)
    }


@router.post("/registro", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para criar um novo usuário no sistema.
    """
    try:
        db_usuario = criar_usuario(db=db, usuario=usuario_data)
        return db_usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=UsuarioOut)
def get_me(
    current_user: Usuario = Depends(get_current_user)
):
    """
    Retorna as informações do usuário autenticado.
    """
    return current_user

