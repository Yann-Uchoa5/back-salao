from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from models.cliente import Cliente
from schemas.cliente import ClienteCreate, ClienteUpdate


def criar_cliente(db: Session, cliente: ClienteCreate) -> Cliente:
    """
    Cria um novo cliente no banco de dados.
    """
    db_cliente = Cliente(nome=cliente.nome)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def get_cliente(db: Session, cliente_id: int) -> Optional[Cliente]:
    """
    Retorna um cliente pelo seu ID.
    """
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def get_clientes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[Cliente]:
    """
    Retorna uma lista de clientes com filtros opcionais.
    """
    query = db.query(Cliente)

    # Filtro por busca de nome
    if search:
        query = query.filter(Cliente.nome.ilike(f"%{search}%"))

    # Ordena por nome
    query = query.order_by(Cliente.nome.asc())

    return query.offset(skip).limit(limit).all()


def atualizar_cliente(
    db: Session,
    cliente_id: int,
    cliente_update: ClienteUpdate
) -> Optional[Cliente]:
    """
    Atualiza as informações de um cliente existente.
    """
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None

    update_data = cliente_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cliente, field, value)

    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def atualizar_foto_cliente(
    db: Session,
    cliente_id: int,
    caminho_foto: str
) -> Optional[Cliente]:
    """
    Atualiza o caminho da foto de um cliente.
    """
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None

    db_cliente.caminho_foto = caminho_foto
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def deletar_cliente(db: Session, cliente_id: int) -> bool:
    """
    Deleta um cliente do banco de dados.
    """
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return False

    db.delete(db_cliente)
    db.commit()
    return True

