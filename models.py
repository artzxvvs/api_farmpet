import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey, event
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# usar URL do .env; fallback para sqlite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farmpet.db")

# engine: passar connect_args para sqlite
if DATABASE_URL.startswith("sqlite"):
    db = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
else:
    db = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=db, expire_on_commit=False)
Base = declarative_base()

# Usuários
class Usuario(Base):
    __tablename__ = "usuarios"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    NOME = Column(String, nullable=False)
    EMAIL = Column(String, nullable=False, unique=True)
    SENHA = Column(String, nullable=False)
    ATIVO = Column(Boolean, default=True)
    ADMIN = Column(Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.NOME = nome
        self.EMAIL = email
        self.SENHA = senha
        self.ATIVO = ativo
        self.ADMIN = admin

# Clientes
class Cliente(Base):
    __tablename__ = "clientes"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    NOME = Column(String, nullable=False)
    ID_USUARIO = Column(Integer, ForeignKey("usuarios.ID"), nullable=True)
    RUA = Column(String, nullable=True)
    NUMERO = Column(String, nullable=True)
    BAIRRO = Column(String, nullable=True)
    COMPLEMENTO = Column(String, nullable=True)
    CPF = Column(String, nullable=True, unique=True)
    TELEFONE = Column(String, nullable=True)

    usuario = relationship("Usuario", foreign_keys=[ID_USUARIO])

# Colaboradores
class Colaborador(Base):
    __tablename__ = "colaboradores"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    NOME = Column(String, nullable=False)
    CPF = Column(String, nullable=False, unique=True)
    TELEFONE = Column(String, nullable=True)
    CARGO = Column(String, nullable=True)

    def __init__(self, nome, cpf, telefone=None, cargo=None):
        self.NOME = nome
        self.CPF = cpf
        self.TELEFONE = telefone
        self.CARGO = cargo

# Pets
class Pet(Base):
    __tablename__ = "pets"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    NOME = Column(String, nullable=False)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID"), nullable=True)
    cliente = relationship("Cliente", foreign_keys=[ID_CLIENTE])

# Remédios
class Remedio(Base):
    __tablename__ = "remedios"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    NOME = Column(String, nullable=False, unique=True)
    DESCRICAO = Column(String, nullable=True)
    PRECO = Column(Float, nullable=False, default=0.0)
    ESTOQUE = Column(Integer, default=0)
    RECEITA = Column(String, nullable=True)

    def __init__(self, nome, descricao, preco, estoque=0, receita=None):
        self.NOME = nome
        self.DESCRICAO = descricao
        self.PRECO = preco
        self.ESTOQUE = estoque
        self.RECEITA = receita

# Brinquedos
class Brinquedo(Base):
    __tablename__ = "brinquedos"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    NOME = Column(String, nullable=False, unique=True)
    CATEGORIA = Column(String, nullable=False)  # Pelúcia, Bola, Interativo, Mordedor
    PRECO = Column(Float, nullable=False, default=0.0)
    IMAGEM = Column(String, nullable=True)
    ESTOQUE = Column(Integer, default=0)
    DESCRICAO = Column(String, nullable=True)

    def __init__(self, nome, categoria, preco, estoque=0, imagem=None, descricao=None):
        self.NOME = nome
        self.CATEGORIA = categoria
        self.PRECO = preco
        self.ESTOQUE = estoque
        self.IMAGEM = imagem
        self.DESCRICAO = descricao

# Transações / Compras
class Transacao(Base):
    __tablename__ = "transacoes"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID"), nullable=False)
    ID_REMEDIO = Column(Integer, ForeignKey("remedios.ID"), nullable=False)
    ID_PET = Column(Integer, ForeignKey("pets.ID"), nullable=True)
    QUANTIDADE = Column(Integer, nullable=False)
    VALOR_DESCONTO = Column(Float, default=0.0)
    VALOR_TOTAL = Column(Float, nullable=True)
    VALOR_FRETE = Column(Float, default=0.0)
    FORMA_PAGAMENTO = Column(String, nullable=True)  # DINHEIRO, PIX, BOLETO, CARTAO_CREDITO, CARTAO_DEBITO
    PARCELAS = Column(Integer, nullable=True)

    remedio = relationship("Remedio", foreign_keys=[ID_REMEDIO])
    cliente = relationship("Cliente", foreign_keys=[ID_CLIENTE])
    pet = relationship("Pet", foreign_keys=[ID_PET])

    def __init__(self, id_cliente, id_remedio, id_pet, quantidade, valor_desconto=0, valor_frete=0, forma_pagamento="DINHEIRO", parcelas=None):
        self.ID_CLIENTE = id_cliente
        self.ID_REMEDIO = id_remedio
        self.ID_PET = id_pet
        self.QUANTIDADE = quantidade
        self.VALOR_DESCONTO = valor_desconto
        self.VALOR_FRETE = valor_frete
        self.FORMA_PAGAMENTO = forma_pagamento
        self.PARCELAS = parcelas

# Normaliza parcelas e calcula valor total antes de persistir
@event.listens_for(Transacao, "before_insert")
@event.listens_for(Transacao, "before_update")
def calcular_valor_total(mapper, connection, target):
    from sqlalchemy.orm import Session
    session = Session(bind=connection)
    remedio = session.get(Remedio, target.ID_REMEDIO)
    if remedio:
        preco_total = (remedio.PRECO or 0) * (target.QUANTIDADE or 0)
        target.VALOR_TOTAL = preco_total - (target.VALOR_DESCONTO or 0) + (target.VALOR_FRETE or 0)

    forma = (target.FORMA_PAGAMENTO or "").upper() if target.FORMA_PAGAMENTO else ""
    if forma == "CARTAO_CREDITO":
        if not target.PARCELAS or target.PARCELAS < 1:
            target.PARCELAS = 1
    else:
        target.PARCELAS = None

    session.close()

# criar tabelas (opcional: comente se usar alembic)
# Base.metadata.create_all(bind=db)


