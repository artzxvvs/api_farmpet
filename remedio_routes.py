from fastapi import APIRouter, Depends, HTTPException
from models import Remedio, db
from dependencies import pegar_sessao
from main import bcrypt_context
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

@remedios_router.post("/Cadastrar_remedio")
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