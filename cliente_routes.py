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


@cliente_router.put("/atualizar_cliente/{cliente_id}")
async def atualizar_cliente(cliente_id: int, session: Session = Depends(pegar_sessao), 
                           nome: str = None, rua: str = None, numero: str = None,
                           bairro: str = None, complemento: str = None, 
                           telefone: str = None, cpf: str = None):
    """
    Atualiza os dados de um cliente existente
    """
    from models import Cliente
    
    cliente = session.query(Cliente).filter(Cliente.ID == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verifica se CPF já está sendo usado por outro cliente
    if cpf and cpf != cliente.CPF:
        cpf_existe = session.query(Cliente).filter(Cliente.CPF == cpf).first()
        if cpf_existe:
            raise HTTPException(status_code=400, detail="CPF já está sendo usado por outro cliente")
    
    try:
        if nome:
            cliente.NOME = nome
        if rua:
            cliente.RUA = rua
        if numero:
            cliente.NUMERO = numero
        if bairro:
            cliente.BAIRRO = bairro
        if complemento:
            cliente.COMPLEMENTO = complemento
        if telefone:
            cliente.TELEFONE = telefone
        if cpf:
            cliente.CPF = cpf
        
        session.commit()
        session.refresh(cliente)
        return {"mensagem": "Cliente atualizado com sucesso", "id": cliente.ID}
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(exc)}")


@cliente_router.delete("/deletar_cliente/{cliente_id}")
async def deletar_cliente(cliente_id: int, session: Session = Depends(pegar_sessao)):
    """
    Deleta um cliente do sistema
    """
    from models import Cliente
    
    cliente = session.query(Cliente).filter(Cliente.ID == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    try:
        session.delete(cliente)
        session.commit()
        return {"mensagem": "Cliente deletado com sucesso", "id": cliente_id}
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar cliente: {str(exc)}")