from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional

PaymentMethod = Literal["DINHEIRO", "PIX", "BOLETO", "CARTAO_CREDITO", "CARTAO_DEBITO"]

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False
    rua: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    complemento: Optional[str] = None
    telefone: Optional[str] = None
    cpf: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "nome": "João",
                "email": "joao@email.com",
                "senha": "123456",
                "ativo": True,
                "admin": False,
                "rua": "Rua A",
                "numero": "123",
                "bairro": "Centro",
                "complemento": "Apto 1",
                "telefone": "11999999999",
                "cpf": "12345678900"
            }
        },
    )

class RemedioSchema(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int
    receita: Optional[bool] = False

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "nome": "Dipirona",
                "descricao": "Analgésico e antipirético",
                "preco": 12.50,
                "estoque": 100,
                "receita": "True"
            }
        },
    )

class Petschema(BaseModel):
    nome: str
    especie: str
    raca: str
    idade: int
    id_cliente: int
    endereco_dono: str = Field(..., alias="endereço_dono")  # aceita também "endereço_dono" no JSON

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True,  # substitui allow_population_by_field_name
        json_schema_extra={
            "example": {
                "nome": "Rex",
                "especie": "Cachorro",
                "raca": "Labrador",
                "idade": 5,
                "id_cliente": 1,
                "endereço_dono": "Rua A, 123"
            }
        },
    )

class Colaboradorchema(BaseModel):
    nome: str
    cpf: str
    telefone: str
    cargo: Optional[str] = None  # Veterinário, Atendente, Estoquista, Entregador

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True,
        json_schema_extra={
            "example": {
                "nome": "Lula inácio da silva",
                "cpf": "12345678900",
                "telefone": "11999999999",
                "cargo": "Veterinário, Atendente, Estoquista, Entregador"
            }
        },
    )

class ClienteSchema(BaseModel):
    nome: str
    rua: str
    numero: str
    bairro: str
    complemento: Optional[str] = None
    telefone: str
    id_usuario: int
    cpf: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "nome": "João",
                "rua": "Rua A",
                "numero": "123",
                "bairro": "Centro",
                "complemento": "Apto 1",
                "telefone": "11999999999",
                "id_usuario": 1,
                "cpf": "12345678900"
            }
        },
    )

class CompraSchema(BaseModel):
    id_cliente: int
    id_remedio: int
    id_pet: Optional[int] = None
    quantidade: int = Field(..., gt=0)
    valor_desconto: Optional[float] = 0.0
    valor_frete: Optional[float] = 0.0
    forma_pagamento: PaymentMethod = Field(..., example="PIX")
    parcelas: Optional[int] = Field(None, example=1, description="Usado somente quando forma_pagamento == CARTAO_CREDITO")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id_cliente": 1,
                "id_remedio": 2,
                "id_pet": 3,
                "quantidade": 2,
                "valor_desconto": 0.0,
                "valor_frete": 10.0,
                "forma_pagamento": "PIX",
                "parcelas": None
            }
        },
    )

class CompraCreate(BaseModel):
    id_cliente: int = Field(..., example=1)
    id_remedio: int = Field(..., example=1)
    id_pet: Optional[int] = Field(None, example=1)
    quantidade: int = Field(..., example=2, gt=0)
    valor_desconto: Optional[float] = Field(0.0, example=0.0)
    valor_frete: Optional[float] = Field(0.0, example=10.0)
    forma_pagamento: PaymentMethod = Field(..., example="PIX")
    parcelas: Optional[int] = Field(None, example=1, description="Usado somente quando forma_pagamento == CARTAO_CREDITO")

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "id_cliente": 1,
                "id_remedio": 1,
                "id_pet": 1,
                "quantidade": 2,
                "valor_desconto": 0.0,
                "valor_frete": 10.0,
                "forma_pagamento": "PIX",
                "parcelas": None
            }
        }
    )


CategoriaBrinquedo = Literal["Pelúcia", "Bola", "Interativo", "Mordedor"]


class BrinquedoSchema(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, example="Urso de Pelúcia")
    categoria: CategoriaBrinquedo = Field(..., example="Pelúcia")
    preco: float = Field(..., gt=0, example=49.90)
    estoque: int = Field(..., ge=0, example=50)
    imagem: Optional[str] = Field(None, example="/imagens/urso-pelucia.png")
    descricao: Optional[str] = Field(None, max_length=500, example="Brinquedo macio e seguro para pets")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "nome": "Urso de Pelúcia",
                "categoria": "Pelúcia",
                "preco": 49.90,
                "estoque": 50,
                "imagem": "/imagens/urso-pelucia.png",
                "descricao": "Brinquedo macio e seguro para pets"
            }
        },
    )
