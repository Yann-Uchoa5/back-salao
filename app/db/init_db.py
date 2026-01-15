"""
Script para inicializar o banco de dados criando todas as tabelas.
Execute este script uma vez para criar as tabelas necessárias.
"""
from db.base import Base
from db.session import engine
from models.usuario import Usuario
from models.cliente import Cliente


def init_db():
    """
    Cria todas as tabelas definidas nos modelos.
    """
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    init_db()

