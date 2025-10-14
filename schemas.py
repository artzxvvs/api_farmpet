from pydantic import BaseModel
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
