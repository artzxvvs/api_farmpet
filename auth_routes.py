from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db,Cliente
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session
from sqlalchemy import select
import pandas as pd

auth_router = APIRouter(prefix="/auth",tags=["auth"])



@auth_router.post("/criar_conta", status_code=201)
async def criar_conta(usuarioschema:UsuarioSchema,session: Session=Depends(pegar_sessao)):
    """Essa é a rota para criar um novo usuário
    - Cria Usuario (hash de senha)
    - Opcionalmente cria Cliente se não for admin
    """
    usuario = session.query(Usuario).filter(Usuario.EMAIL == usuarioschema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email do usuário já cadastrado")

    try:
        senha_criptografada = bcrypt_context.hash(usuarioschema.senha)
        novo_usuario = Usuario(usuarioschema.nome, usuarioschema.email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)  # Garante que ID está disponível

        # Se não for admin, cria cliente associado (verifica campos mínimos)
        if not getattr(usuarioschema, 'admin', False):
            campos_obrigatorios = ['nome', 'rua', 'numero', 'bairro', 'telefone', 'cpf']
            for campo in campos_obrigatorios:
                if not getattr(usuarioschema, campo, None):
                    raise HTTPException(status_code=400, detail=f"Campo obrigatório '{campo}' não informado para cliente.")

            novo_cliente = Cliente(
                usuarioschema.nome,
                usuarioschema.rua,
                usuarioschema.numero,
                usuarioschema.bairro,
                usuarioschema.complemento,
                usuarioschema.telefone,
                novo_usuario.ID,
                usuarioschema.cpf,
            )
            session.add(novo_cliente)
            session.commit()

        return {"mensagem": f"Usuário criado com sucesso {usuarioschema.email}", "id": novo_usuario.ID}
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(exc)}")
    
@auth_router.patch("/alterar_senha")
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








@auth_router.post("/login")
async def Login(usuarioschema:UsuarioSchema,session: Session=Depends(pegar_sessao)):
    """
    Essa é a rota para fazer login
    """
    usuario = session.query(Usuario).filter(Usuario.EMAIL==usuarioschema.email).first()
    if not usuario:
        raise HTTPException(status_code=404,detail="Email do usuário não cadastrado")
    if not bcrypt_context.verify(usuarioschema.senha,usuario.SENHA):
        raise HTTPException(status_code=401,detail="Senha incorreta")
    return {"mensagem": f"Login realizado com sucesso {usuarioschema.email}", "id": usuario.ID}
