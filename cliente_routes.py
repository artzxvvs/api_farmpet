from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session


cliente_router = APIRouter(prefix="/cliente",tags=["cliente"])

@cliente_router.get("/")
async def cliente():
    """
    Essa é a rota padrão de clientes
    """
    return {"mensagem": "Você acaba de acessar a rota de clientes, meus parabéns!!"}


# Alterar senha 

@cliente_router.patch("/alterar_senha")
async def alterar_senha(usuarioschema:UsuarioSchema,session: Session=Depends(pegar_sessao)):
    """
    Essa é a rota para alterar a senha do usuário
    """
    usuario = session.query(Usuario).filter(Usuario.EMAIL==usuarioschema.email).first()
    if not usuario:
        raise HTTPException(status_code=400,detail="Email do usuário não cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuarioschema.senha)
        usuario.SENHA = senha_criptografada
        session.add(usuario)
        session.commit()
        return {"mensagem": f"Senha alterada com sucesso {usuarioschema.email}"}