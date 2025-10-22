from pydantic import BaseModel, Field
from typing import Optional

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

    class Config():
        from_attributes = True
        json_schema_extra = {
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
        }

class RemedioSchema(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int
    receita: Optional[bool] = False
    class Config():
        from_attributes = True
        json_schema_extra = {
            "example": {
                "nome": "Dipirona",
                "descricao": "Analgésico e antipirético",
                "preco": 12.50,
                "estoque": 100,
                "receita": "True"
            }
        }

class Petschema(BaseModel):
    nome: str
    especie: str
    raca: str
    idade: int
    id_cliente: int
    endereco_dono: str = Field(..., alias="endereço_dono")  # aceita também "endereço_dono" no JSON

    class Config():
        from_attributes = True
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "nome": "Rex",
                "especie": "Cachorro",
                "raca": "Labrador",
                "idade": 5,
                "id_cliente": 1,
                "endereço_dono": "Rua A, 123"
            }
        }



class Colaboradorchema(BaseModel):
    nome: str
    cpf: str
    telefone: str
    cargo: Optional[str] = None  # Veterinário, Atendente, Estoquista, Entregador
    
    class Config():
        from_attributes = True
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "nome": "Lula inácio da silva",
                "cpf": "12345678900",
                "telefone": "11999999999",
                "cargo": "Veterinário, Atendente, Estoquista, Entregador"
            }
        }