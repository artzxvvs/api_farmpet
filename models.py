from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

# Criar conexão engine
db = create_engine("sqlite:///banco.db")

# Criar base db
Base = declarative_base()

# Criar classes/tabelas do banco de dados
# Usuarios
class Usuario(Base):
    __tablename__ = "usuarios"
    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    NOME = Column("NOME", String, nullable=False)
    EMAIL =  Column("EMAIL", String, nullable=False, unique=True)
    SENHA = Column("SENHA", String, nullable=False) 
    ATIVO = Column("ATIVO", Boolean)
    ADMIN = Column("ADMIN", Boolean,default=False) 

    def __init__(self,nome,email,senha,ativo=True,admin=False):
        self.NOME = nome
        self.EMAIL = email
        self.SENHA = senha
        self.ATIVO = ativo
        self.ADMIN = admin

# Clientes

class Cliente(Base):
    __tablename__ = "clientes"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome = Column("NOME",String, nullable=False)
    id_usuario = Column("ID_USUARIO", Integer, ForeignKey("usuarios.ID"), nullable=False)
    rua = Column("RUA", String, nullable=False)
    numero = Column("NUMERO", String, nullable=False)
    bairro = Column("BAIRRO", String, nullable=False)
    complemento = Column("COMPLEMENTO", String)
    cpf = Column("CPF", String, nullable=False, unique=True)
    telefone = Column("TELEFONE", String, nullable=False)

    def __init__(self, nome, rua, numero, bairro, complemento, telefone, id_usuario, cpf):
        self.nome = nome
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.complemento = complemento
        self.telefone = telefone
        self.id_usuario = id_usuario
        self.cpf = cpf
# Colaborador
class Colaborador(Base):
    __tablename__ = "colaboradores"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    NOME = Column("NOME", String, nullable=False)
    CPF = Column("CPF", String, nullable=False, unique=True)
    TELEFONE = Column("TELEFONE", String, nullable=False)
    CARGO = Column("CARGO", String) # Veterinário, Atendente, Estoquista, Entregador

    def __init__(self,nome,cargo,cpf,telefone):
        self.NOME = nome
        self.CPF = cpf
        self.TELEFONE = telefone
        self.CARGO = cargo
    def __init__(self, nome, cpf, telefone, cargo=None):
        self.NOME = nome
        self.CPF = cpf
        self.TELEFONE = telefone
        self.CARGO = cargo
    def __init__(self, nome: str, cpf: str, telefone: str, cargo: str | None = None):
        # Use apenas keyword args na criação para evitar confusão posicional
       self.NOME = nome
       self.CPF = cpf
       self.TELEFONE = telefone
       self.CARGO = cargo
# Pets
class Pet(Base):
    __tablename__ = "pets"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    NOME_PET = Column("NOME", String, nullable=False)
    ESPECIE = Column("ESPECIE", String, nullable=False)
    RACA = Column("RACA", String, nullable=False)
    ENDERECO_DONO = Column("ENDERECO_DONO", String, nullable=False)
    CLIENTE_ID = Column("CLIENTE_ID", Integer, ForeignKey("clientes.ID"), nullable=False)

    def __init__(self, nome, especie, raca, endereco_dono, cliente_id):
        self.NOME_PET = nome
        self.ESPECIE = especie
        self.RACA = raca
        self.ENDERECO_DONO = endereco_dono
        self.CLIENTE_ID = cliente_id
# Remédios
class Remedio(Base):
    __tablename__ = "remedios"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    NOME = Column("NOME", String, nullable=False)
    DESCRICAO = Column("DESCRICAO", String, nullable=False)
    PRECO = Column("PRECO", Float, nullable=False)
    ESTOQUE = Column("ESTOQUE", Integer, nullable=False)
    RECEITA = Column("RECEITA", String)

    def __init__(self,nome,descricao,preco,estoque,receita):
        self.NOME = nome
        self.DESCRICAO = descricao
        self.PRECO = preco
        self.ESTOQUE = estoque
        self.RECEITA = receita

# executar a criação dos metadados do seu banco (Criar efetivamento o banco de dados)


