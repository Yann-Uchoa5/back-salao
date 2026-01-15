from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import os
import shutil
import uuid
from pathlib import Path

from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut, ClienteComProcedimentosOut
from crud.cliente import (
    criar_cliente,
    get_cliente,
    get_clientes,
    atualizar_cliente,
    deletar_cliente,
    atualizar_foto_cliente
)
from core.dependencies import get_db, get_current_active_admin
from models.usuario import Usuario

router = APIRouter()

# Define o diretório para salvar as fotos e o cria se não existir
UPLOAD_DIR = "uploads/clientes/fotos/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Tipos de arquivo permitidos (apenas imagens)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


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
    
    Exemplo de JSON:
    {
        "nome": "Maria Silva"
    }
    
    Nota: Para adicionar procedimentos, use o endpoint POST /api/v1/procedimentos/
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
    search: Optional[str] = Query(None, description="Buscar por nome do cliente")
):
    """
    Retorna uma lista de todos os clientes cadastrados, com filtros opcionais.
    """
    clientes = get_clientes(
        db=db,
        skip=skip,
        limit=limit,
        search=search
    )
    return clientes


@router.get("/{cliente_id}/historico", response_model=ClienteComProcedimentosOut)
def get_cliente_com_historico_route(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna um cliente com seu histórico completo de procedimentos.
    """
    from crud.procedimento import get_procedimentos
    from schemas.procedimento import ProcedimentoOut
    
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Busca todos os procedimentos do cliente
    procedimentos = get_procedimentos(db=db, cliente_id=cliente_id, limit=1000)
    
    # Converte para o schema de saída
    cliente_out = ClienteOut.model_validate(db_cliente)
    procedimentos_out = [ProcedimentoOut.model_validate(p) for p in procedimentos]
    
    return ClienteComProcedimentosOut(
        **cliente_out.model_dump(),
        procedimentos=procedimentos_out
    )


@router.get("/{cliente_id}", response_model=ClienteOut)
def get_cliente_route(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna as informações básicas de um cliente específico pelo seu ID.
    Para obter o histórico completo de procedimentos, use GET /{cliente_id}/historico
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
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Remove a foto se existir
    if db_cliente.caminho_foto and os.path.exists(db_cliente.caminho_foto):
        try:
            os.remove(db_cliente.caminho_foto)
        except Exception:
            pass  # Ignora erros ao deletar arquivo
    
    success = deletar_cliente(db, cliente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return None


@router.post("/{cliente_id}/foto", response_model=ClienteOut, status_code=status.HTTP_200_OK)
def upload_foto_cliente(
    cliente_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_admin)
):
    """
    Faz upload de uma foto para um cliente específico.
    
    Aceita apenas arquivos de imagem (jpg, jpeg, png, gif, webp).
    Tamanho máximo: 5MB
    """
    # Verifica se o cliente existe
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Valida a extensão do arquivo
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo não permitido. Tipos aceitos: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Lê o conteúdo do arquivo para verificar o tamanho
    file_content = file.file.read()
    file_size = len(file_content)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE / (1024 * 1024):.1f}MB"
        )
    
    # Gera um nome único para o arquivo
    file_id = str(uuid.uuid4())
    file_name = f"{cliente_id}_{file_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    try:
        # Remove a foto antiga se existir
        if db_cliente.caminho_foto and os.path.exists(db_cliente.caminho_foto):
            try:
                os.remove(db_cliente.caminho_foto)
            except Exception:
                pass  # Ignora erros ao deletar arquivo antigo
        
        # Salva o novo arquivo
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # Atualiza o caminho da foto no banco de dados
        db_cliente = atualizar_foto_cliente(db, cliente_id, file_path)
        if not db_cliente:
            # Se falhar, remove o arquivo que foi salvo
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail="Erro ao atualizar foto no banco de dados")
        
        return db_cliente
        
    except Exception as e:
        # Remove o arquivo se houver erro
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar a foto: {str(e)}"
        )


@router.get("/{cliente_id}/foto")
def get_foto_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna a foto de um cliente específico.
    """
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    if not db_cliente.caminho_foto:
        raise HTTPException(status_code=404, detail="Cliente não possui foto cadastrada")
    
    # Verifica se o arquivo existe
    if not os.path.exists(db_cliente.caminho_foto):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Arquivo de foto não encontrado no servidor. Contate o administrador."
        )
    
    # Determina o tipo MIME baseado na extensão
    file_extension = Path(db_cliente.caminho_foto).suffix.lower()
    media_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }
    media_type = media_type_map.get(file_extension, "image/jpeg")
    
    return FileResponse(
        path=db_cliente.caminho_foto,
        media_type=media_type,
        filename=f"foto_cliente_{cliente_id}{file_extension}"
    )

