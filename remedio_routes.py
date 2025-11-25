from fastapi import APIRouter, Depends, HTTPException
from models import Remedio, db
from dependencies import pegar_sessao
from security import bcrypt_context
from schemas import RemedioSchema
from sqlalchemy.orm import Session
from sqlalchemy import select
import pandas as pd

remedios_router = APIRouter(prefix="/remedios", tags=["Remedios"])

@remedios_router.get("/")
async def listar_remedios():
    conn = db.connect()
    with conn as con:
        query = select(Remedio)
        result = pd.read_sql(query, con)
        result = result.to_dict(orient='records')

    """
    Essa é a rota para listar todos os remédios
    """
    return {"mensagem": "Lista de remédios acessada com sucesso!", "data": result}

@remedios_router.post("/Cadastrar_remedio", status_code=201)
async def criar_remedio(remedio: RemedioSchema, session: Session = Depends(pegar_sessao)):
    existente = session.query(Remedio).filter(Remedio.NOME == remedio.nome).first()
    if existente:
        raise HTTPException(status_code=400, detail="Remédio já cadastrado no sistema, seguir a atualização de estoque")
    try:
        # converter receita para string (o modelo Remedio armazena RECEITA como String)
        receita_val = str(remedio.receita) if remedio.receita is not None else None
        novo_remedio = Remedio(remedio.nome, remedio.descricao, remedio.preco, remedio.estoque, receita_val)
        session.add(novo_remedio)
        session.commit()
        session.refresh(novo_remedio)  # Garante que ID está disponível
        return {"mensagem": f"Remédio cadastrado com sucesso: {novo_remedio.NOME}", "id": novo_remedio.ID}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@remedios_router.put("/atualizar_remedio/{remedio_id}")
async def atualizar_remedio(remedio_id: int, remedio: RemedioSchema, session: Session = Depends(pegar_sessao)):
    """
    Atualiza os dados de um remédio existente
    """
    remedio_existente = session.query(Remedio).filter(Remedio.ID == remedio_id).first()
    if not remedio_existente:
        raise HTTPException(status_code=404, detail="Remédio não encontrado")
    
    # Verifica se o nome já está sendo usado por outro remédio
    if remedio.nome != remedio_existente.NOME:
        nome_existe = session.query(Remedio).filter(Remedio.NOME == remedio.nome).first()
        if nome_existe:
            raise HTTPException(status_code=400, detail="Nome do remédio já está sendo usado")
    
    try:
        remedio_existente.NOME = remedio.nome
        remedio_existente.DESCRICAO = remedio.descricao
        remedio_existente.PRECO = remedio.preco
        remedio_existente.ESTOQUE = remedio.estoque
        remedio_existente.RECEITA = str(remedio.receita) if remedio.receita is not None else None
        
        session.commit()
        session.refresh(remedio_existente)
        return {"mensagem": "Remédio atualizado com sucesso", "id": remedio_existente.ID}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar remédio: {str(e)}")


@remedios_router.delete("/deletar_remedio/{remedio_id}")
async def deletar_remedio(remedio_id: int, session: Session = Depends(pegar_sessao)):
    """
    Deleta um remédio do sistema
    """
    remedio = session.query(Remedio).filter(Remedio.ID == remedio_id).first()
    if not remedio:
        raise HTTPException(status_code=404, detail="Remédio não encontrado")
    
    try:
        session.delete(remedio)
        session.commit()
        return {"mensagem": "Remédio deletado com sucesso", "id": remedio_id}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar remédio: {str(e)}")