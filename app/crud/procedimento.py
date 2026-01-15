from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import date

from models.procedimento import Procedimento
from models.cliente import Cliente
from schemas.procedimento import ProcedimentoCreate, ProcedimentoUpdate


def criar_procedimento(db: Session, procedimento: ProcedimentoCreate) -> Procedimento:
    """
    Cria um novo procedimento para um cliente.
    """
    # Verifica se o cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == procedimento.cliente_id).first()
    if not cliente:
        raise ValueError("Cliente não encontrado")
    
    db_procedimento = Procedimento(
        cliente_id=procedimento.cliente_id,
        data_procedimento=procedimento.data_procedimento,
        tipo_procedimento=procedimento.tipo_procedimento,
        qtd_tonalizante=procedimento.qtd_tonalizante,
        valor_procedimento=procedimento.valor_procedimento,
        observacao=procedimento.observacao,
        corte=procedimento.corte
    )
    db.add(db_procedimento)
    db.commit()
    db.refresh(db_procedimento)
    return db_procedimento


def get_procedimento(db: Session, procedimento_id: int) -> Optional[Procedimento]:
    """
    Retorna um procedimento pelo seu ID.
    """
    return db.query(Procedimento).filter(Procedimento.id == procedimento_id).first()


def get_procedimentos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    cliente_id: Optional[int] = None,
    search: Optional[str] = None,
    tipo_procedimento: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    corte: Optional[bool] = None
) -> List[Procedimento]:
    """
    Retorna uma lista de procedimentos com filtros opcionais.
    """
    query = db.query(Procedimento)

    # Filtro por cliente
    if cliente_id:
        query = query.filter(Procedimento.cliente_id == cliente_id)

    # Filtro por busca (tipo de procedimento ou observação)
    if search:
        query = query.filter(
            or_(
                Procedimento.tipo_procedimento.ilike(f"%{search}%"),
                Procedimento.observacao.ilike(f"%{search}%")
            )
        )

    # Filtro por tipo de procedimento
    if tipo_procedimento:
        query = query.filter(Procedimento.tipo_procedimento.ilike(f"%{tipo_procedimento}%"))

    # Filtro por data (período)
    if data_inicio:
        query = query.filter(Procedimento.data_procedimento >= data_inicio)
    if data_fim:
        query = query.filter(Procedimento.data_procedimento <= data_fim)

    # Filtro por corte
    if corte is not None:
        query = query.filter(Procedimento.corte == corte)

    # Ordena por data do procedimento (mais recente primeiro)
    query = query.order_by(Procedimento.data_procedimento.desc())

    return query.offset(skip).limit(limit).all()


def atualizar_procedimento(
    db: Session,
    procedimento_id: int,
    procedimento_update: ProcedimentoUpdate
) -> Optional[Procedimento]:
    """
    Atualiza as informações de um procedimento existente.
    """
    db_procedimento = get_procedimento(db, procedimento_id)
    if not db_procedimento:
        return None

    update_data = procedimento_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_procedimento, field, value)

    db.commit()
    db.refresh(db_procedimento)
    return db_procedimento


def deletar_procedimento(db: Session, procedimento_id: int) -> bool:
    """
    Deleta um procedimento do banco de dados.
    """
    db_procedimento = get_procedimento(db, procedimento_id)
    if not db_procedimento:
        return False

    db.delete(db_procedimento)
    db.commit()
    return True

