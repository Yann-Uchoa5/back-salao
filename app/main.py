from fastapi import FastAPI
from v1 import cliente, login

app = FastAPI(
    title="Sistema de Salão - API",
    description="API para gerenciamento de clientes e procedimentos do salão",
    version="1.0.0"
)

# Registrar os routers
app.include_router(login.router, prefix="/api/v1/auth", tags=["Autenticação"])
app.include_router(cliente.router, prefix="/api/v1/clientes", tags=["Clientes"])


@app.get("/")
def root():
    return {"message": "API do Sistema de Salão"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

