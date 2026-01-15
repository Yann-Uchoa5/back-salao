from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from schemas.procedimento import ProcedimentoCreate, ProcedimentoUpdate, ProcedimentoOut
from crud.procedimento import (
    criar_procedimento,
    get_procedimento,
    get_procedimentos,
    atualizar_procedimento,
    deletar_procedimento
)
from core.dependencies import get_db, get_current_user, get_current_active_admin
from models.usuario import Usuario

router = APIRouter()


@router.post("/", response_model=ProcedimentoOut, status_code=status.HTTP_201_CREATED)
def criar_procedimento_route(
    procedimento_data: ProcedimentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cria um novo procedimento para um cliente.
    
    Campos obrigatórios:
    - cliente_id: int (ID do cliente)
    - data_procedimento: date (formato YYYY-MM-DD, ex: "2024-01-15")
    - tipo_procedimento: string (mínimo 1 caractere)
    - valor_procedimento: float (deve ser >= 0)
    
    Campos opcionais:
    - qtd_tonalizante: float (deve ser >= 0)
    - observacao: string (máximo 1000 caracteres)
    - corte: boolean (padrão: false)
    
    Exemplo de JSON:
    {
        "cliente_id": 1,
        "data_procedimento": "2024-01-15",
        "tipo_procedimento": "Coloração",
        "valor_procedimento": 150.00,
        "qtd_tonalizante": 50.5,
        "observacao": "Cliente satisfeita",
        "corte": true
    }
    """
    try:
        db_procedimento = criar_procedimento(db=db, procedimento=procedimento_data)
        return db_procedimento
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar procedimento: {str(e)}"
        )


@router.get("/", response_model=List[ProcedimentoOut])
def listar_procedimentos_route(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, le=100, description="Número máximo de registros a retornar"),
    cliente_id: Optional[int] = Query(None, description="Filtrar por ID do cliente"),
    search: Optional[str] = Query(None, description="Buscar por tipo de procedimento ou observação"),
    tipo_procedimento: Optional[str] = Query(None, description="Filtrar por tipo de procedimento"),
    data_inicio: Optional[date] = Query(None, description="Data inicial do período (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(None, description="Data final do período (YYYY-MM-DD)"),
    corte: Optional[bool] = Query(None, description="Filtrar por procedimentos com corte")
):
    """
    Retorna uma lista de procedimentos cadastrados, com filtros opcionais.
    """
    procedimentos = get_procedimentos(
        db=db,
        skip=skip,
        limit=limit,
        cliente_id=cliente_id,
        search=search,
        tipo_procedimento=tipo_procedimento,
        data_inicio=data_inicio,
        data_fim=data_fim,
        corte=corte
    )
    return procedimentos


@router.get("/{procedimento_id}", response_model=ProcedimentoOut)
def get_procedimento_route(
    procedimento_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna as informações de um procedimento específico pelo seu ID.
    """
    db_procedimento = get_procedimento(db, procedimento_id)
    if db_procedimento is None:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")
    return db_procedimento


@router.put("/{procedimento_id}", response_model=ProcedimentoOut)
def atualizar_procedimento_route(
    procedimento_id: int,
    procedimento_update: ProcedimentoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    """
    Atualiza as informações de um procedimento existente.
    """
    db_procedimento = atualizar_procedimento(db, procedimento_id, procedimento_update)
    if db_procedimento is None:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")
    return db_procedimento


@router.delete("/{procedimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_procedimento_route(
    procedimento_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    """
    Deleta um procedimento do banco de dados pelo seu ID.
    """
    success = deletar_procedimento(db, procedimento_id)
    if not success:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")
    return None

