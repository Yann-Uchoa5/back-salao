from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from crud.cliente import (
    criar_cliente,
    get_cliente,
    get_clientes,
    atualizar_cliente,
    deletar_cliente
)
from core.dependencies import get_db, get_current_active_admin
from models.usuario import Usuario

router = APIRouter()


@router.post("/", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
def criar_cliente_route(
    cliente_data: ClienteCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_admin)
):
    """
    Cria um novo cliente no sistema.
    
    Campos obrigatórios:
    - nome: string (mínimo 1 caractere)
    - data_procedimento: date (formato YYYY-MM-DD, ex: "2024-01-15")
    - tipo_procedimento: string (mínimo 1 caractere)
    - valor_procedimento: float (deve ser >= 0)
    
    Campos opcionais:
    - qtd_tonalizante: float (deve ser >= 0)
    - observacao: string (máximo 1000 caracteres)
    - corte: boolean (padrão: false)
    
    Exemplo de JSON:
    {
        "nome": "Maria Silva",
        "data_procedimento": "2024-01-15",
        "tipo_procedimento": "Coloração",
        "valor_procedimento": 150.00,
        "qtd_tonalizante": 50.5,
        "observacao": "Cliente satisfeita",
        "corte": true
    }
    """
    try:
        db_cliente = criar_cliente(db=db, cliente=cliente_data)
        return db_cliente
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar cliente: {str(e)}"
        )


@router.get("/", response_model=List[ClienteOut])
def listar_clientes_route(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, le=100, description="Número máximo de registros a retornar"),
    search: Optional[str] = Query(None, description="Buscar por nome ou tipo de procedimento"),
    tipo_procedimento: Optional[str] = Query(None, description="Filtrar por tipo de procedimento"),
    data_inicio: Optional[date] = Query(None, description="Data inicial do período (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(None, description="Data final do período (YYYY-MM-DD)"),
    corte: Optional[bool] = Query(None, description="Filtrar por procedimentos com corte")
):
    """
    Retorna uma lista de todos os clientes cadastrados, com filtros opcionais.
    """
    clientes = get_clientes(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        tipo_procedimento=tipo_procedimento,
        data_inicio=data_inicio,
        data_fim=data_fim,
        corte=corte
    )
    return clientes


@router.get("/{cliente_id}", response_model=ClienteOut)
def get_cliente_route(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna as informações de um cliente específico pelo seu ID.
    """
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente


@router.put("/{cliente_id}", response_model=ClienteOut)
def atualizar_cliente_route(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_admin)
):
    """
    Atualiza as informações de um cliente existente.
    """
    db_cliente = atualizar_cliente(db, cliente_id, cliente_update)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente_route(
    cliente_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_admin)
):
    """
    Deleta um cliente do banco de dados pelo seu ID.
    """
    success = deletar_cliente(db, cliente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return None

