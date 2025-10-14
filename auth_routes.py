from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session
from sqlalchemy import select
import pandas as pd

auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.get("/")
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

@auth_router.post("/criar_conta")
async def criar_conta(usuarioschema:UsuarioSchema,session: Session=Depends(pegar_sessao)):
    """
    Essa é a rota para criar um novo usuário
    """
    usuario = session.query(Usuario).filter(Usuario.EMAIL==usuarioschema.email).first()
    if usuario:
        raise HTTPException(status_code=400,detail="Email do usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuarioschema.senha)
        novo_usuario = Usuario(usuarioschema.nome,usuarioschema.email,senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário criado com sucesso {usuarioschema.email}"}
    
@auth_router.patch("/alterar_senha")
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








@auth_router.post("/login")
async def Login(usuarioschema:UsuarioSchema,session: Session=Depends(pegar_sessao)):
    """
    Essa é a rota para fazer login
    """
    usuario = session.query(Usuario).filter(Usuario.EMAIL==usuarioschema.email).first()
    if not usuario:
        raise HTTPException(status_code=400,detail="Email do usuário não cadastrado")
    elif not bcrypt_context.verify(usuarioschema.senha,usuario.SENHA):
        raise HTTPException(status_code=400,detail="Senha incorreta")
    else:
        return {"mensagem": f"Login realizado com sucesso {usuarioschema.email}"}
     