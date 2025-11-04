from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from dependencies import pegar_sessao
from security import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session
from sqlalchemy import select
import pandas as pd


cliente_router = APIRouter(prefix="/cliente",tags=["cliente"])

@cliente_router.get("/")
async def autenticar():
    conn=db.connect()
    with conn as con:
        query= select(Usuario)
        result= pd.read_sql(query,con)
        result=result.to_dict(orient='records')

    """
    Essa é a rota padrão de autenticação
    """
    return {"mensagem": "Você acaba de acessar a rota de autenticação, meus parabéns!","data":result}







# Alterar senha 

@cliente_router.patch("/alterar_senha")
async def alterar_senha(usuarioschema:UsuarioSchema,session: Session=Depends(pegar_sessao)):
    """
    Essa é a rota para alterar a senha do usuário
    """
    usuario = session.query(Usuario).filter(Usuario.EMAIL==usuarioschema.email).first()
    if not usuario:
        raise HTTPException(status_code=404,detail="Email do usuário não cadastrado")
    senha_criptografada = bcrypt_context.hash(usuarioschema.senha)
    usuario.SENHA = senha_criptografada
    session.add(usuario)
    session.commit()
    return {"mensagem": f"Senha alterada com sucesso {usuarioschema.email}"}