from sqlalchemy.orm import Session
from typing import Optional
from passlib.context import CryptContext
from models.usuario import Usuario
from schemas.login import UsuarioCreate

# Configuração para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Gera o hash da senha.
    """
    return pwd_context.hash(password)


def get_usuario_by_username(db: Session, username: str) -> Optional[Usuario]:
    """
    Busca um usuário pelo nome de usuário.
    """
    return db.query(Usuario).filter(Usuario.username == username).first()


def get_usuario_by_email(db: Session, email: str) -> Optional[Usuario]:
    """
    Busca um usuário pelo email.
    """
    return db.query(Usuario).filter(Usuario.email == email).first()


def get_usuario_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
    """
    Busca um usuário pelo ID.
    """
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def autenticar_usuario(db: Session, username: str, password: str) -> Optional[Usuario]:
    """
    Autentica um usuário verificando username e senha.
    Retorna o usuário se as credenciais estiverem corretas, None caso contrário.
    """
    usuario = get_usuario_by_username(db, username)
    if not usuario:
        return None
    
    if not verify_password(password, usuario.hashed_password):
        return None
    
    if not usuario.is_active:
        return None
    
    return usuario


def criar_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
    """
    Cria um novo usuário no banco de dados.
    """
    # Verifica se já existe usuário com mesmo username ou email
    if get_usuario_by_username(db, usuario.username):
        raise ValueError("Username já está em uso")
    
    if get_usuario_by_email(db, usuario.email):
        raise ValueError("Email já está em uso")
    
    hashed_password = get_password_hash(usuario.password)
    
    db_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        nome_completo=usuario.nome_completo,
        hashed_password=hashed_password,
        is_admin=usuario.is_admin,
        is_active=True
    )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

