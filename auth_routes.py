from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db,Cliente
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session
from sqlalchemy import select
import pandas as pd

auth_router = APIRouter(prefix="/auth",tags=["auth"])



@auth_router.post("/criar_conta")
async def criar_conta(usuarioschema:UsuarioSchema,session: Session=Depends(pegar_sessao)):
    """
    Essa é a rota para criar um novo usuário
    """
    usuario = session.query(Usuario).filter(Usuario.EMAIL==usuarioschema.email).first()
    if usuario:
        raise HTTPException(status_code=400,detail="Email do usuário já cadastrado")
    try:
        senha_criptografada = bcrypt_context.hash(usuarioschema.senha)
        novo_usuario = Usuario(usuarioschema.nome,usuarioschema.email,senha_criptografada)
        data_dict= dict(usuarioschema)
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)  # Garante que ID está disponível

        if data_dict.get('admin', False) == False:
            # Verifica se todos os campos obrigatórios para Cliente estão presentes
            campos_obrigatorios = ['nome', 'rua', 'numero', 'bairro', 'telefone', 'cpf']
            for campo in campos_obrigatorios:
                if not getattr(usuarioschema, campo, None):
                    raise HTTPException(status_code=400, detail=f"Campo obrigatório '{campo}' não informado para cliente.")

            novo_cliente= Cliente(
                usuarioschema.nome,
                usuarioschema.rua,
                usuarioschema.numero,
                usuarioschema.bairro,
                usuarioschema.complemento,
                usuarioschema.telefone,
                novo_usuario.ID,
                usuarioschema.cpf
            )
            session.add(novo_cliente)
            session.commit()
        return {"mensagem": f"Usuário criado com sucesso {usuarioschema.email}"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")
    
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
