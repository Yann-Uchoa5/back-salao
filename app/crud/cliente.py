from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from datetime import date

from models.cliente import Cliente
from schemas.cliente import ClienteCreate, ClienteUpdate


def criar_cliente(db: Session, cliente: ClienteCreate) -> Cliente:
    """
    Cria um novo cliente no banco de dados.
    """
    db_cliente = Cliente(
        nome=cliente.nome,
        data_procedimento=cliente.data_procedimento,
        tipo_procedimento=cliente.tipo_procedimento,
        qtd_tonalizante=cliente.qtd_tonalizante,
        valor_procedimento=cliente.valor_procedimento,
        observacao=cliente.observacao,
        corte=cliente.corte
    )
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
    search: Optional[str] = None,
    tipo_procedimento: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    corte: Optional[bool] = None
) -> List[Cliente]:
    """
    Retorna uma lista de clientes com filtros opcionais.
    """
    query = db.query(Cliente)

    # Filtro por busca de nome
    if search:
        query = query.filter(
            or_(
                Cliente.nome.ilike(f"%{search}%"),
                Cliente.tipo_procedimento.ilike(f"%{search}%")
            )
        )

    # Filtro por tipo de procedimento
    if tipo_procedimento:
        query = query.filter(Cliente.tipo_procedimento.ilike(f"%{tipo_procedimento}%"))

    # Filtro por data (período)
    if data_inicio:
        query = query.filter(Cliente.data_procedimento >= data_inicio)
    if data_fim:
        query = query.filter(Cliente.data_procedimento <= data_fim)

    # Filtro por corte
    if corte is not None:
        query = query.filter(Cliente.corte == corte)

    # Ordena por data do procedimento (mais recente primeiro)
    query = query.order_by(Cliente.data_procedimento.desc())

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

