from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from v1 import cliente, login, procedimento
from db.base import Base
from db.session import engine
from models.usuario import Usuario
from models.cliente import Cliente
from models.procedimento import Procedimento

app = FastAPI(
    title="Sistema de Salão - API",
    description="API para gerenciamento de clientes e procedimentos do salão",
    version="1.0.0"
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React padrão
        "http://localhost:5173",  # Vite padrão
        "http://localhost:5174",  # Vite alternativo
        "http://localhost:8080",  # Vue padrão
        "http://localhost:4200",  # Angular padrão
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler personalizado para erros de validação, retorna mensagens mais claras.
    """
    errors = []
    for error in exc.errors():
        # Extrai o caminho do campo
        field_path = error["loc"]
        # Remove "body" do início se existir
        field = ".".join(str(loc) for loc in field_path if loc != "body")
        
        errors.append({
            "campo": field if field else "body",
            "mensagem": error["msg"],
            "tipo": error["type"],
            "valor_recebido": error.get("input")
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Erro de validação nos dados enviados",
            "erros": errors
        }
    )

# Criar tabelas automaticamente ao iniciar (apenas se não existirem)
@app.on_event("startup")
def on_startup():
    """
    Cria as tabelas no banco de dados quando a aplicação inicia.
    """
    Base.metadata.create_all(bind=engine)

# Registrar os routers
app.include_router(login.router, prefix="/api/v1/auth", tags=["Autenticação"])
app.include_router(cliente.router, prefix="/api/v1/clientes", tags=["Clientes"])
app.include_router(procedimento.router, prefix="/api/v1/procedimentos", tags=["Procedimentos"])


@app.get("/")
def root():
    return {"message": "API do Sistema de Salão"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

