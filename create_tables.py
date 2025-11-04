"""Script de conveniência para criar tabelas do banco de dados usando SQLAlchemy.

Use este script em desenvolvimento para criar as tabelas definidas em `models.py`.
Em produção, prefira usar Alembic (`alembic upgrade head`).
"""
from models import Base, db


def main():
    print("Criando tabelas no banco de dados (se não existirem)...")
    Base.metadata.create_all(bind=db)
    print("Tabelas criadas/confirmadas com sucesso.")


if __name__ == "__main__":
    main()
