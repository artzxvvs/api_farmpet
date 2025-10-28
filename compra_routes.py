from fastapi import APIRouter, Depends, HTTPException
from models import Pet, Remedio, Cliente, Transacao, db
from dependencies import pegar_sessao
from schemas import CompraCreate
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import pandas as pd


compra_router = APIRouter(prefix="/compras", tags=["Compras"])


@compra_router.get("/")
async def listar_compras():
    conn = db.connect()
    with conn as con:
        query = select(Transacao)
        result = pd.read_sql(query, con)
        result = result.to_dict(orient='records')

    return {"mensagem": "Lista de compras acessada com sucesso!", "data": result}


@compra_router.post("/criar", status_code=201)
async def criar_compra(compra: CompraCreate, session: Session = Depends(pegar_sessao)):
    # Valida se cliente existe
    cliente = session.get(Cliente, compra.id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Valida se remedio existe
    remedio = session.get(Remedio, compra.id_remedio)
    if not remedio:
        raise HTTPException(status_code=404, detail="Remédio não encontrado")

    # Se forneceu pet, valida
    if compra.id_pet is not None:
        pet_obj = session.get(Pet, compra.id_pet)
        if not pet_obj:
            raise HTTPException(status_code=404, detail="Pet não encontrado")

    # Verifica estoque
    if remedio.ESTOQUE < compra.quantidade:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

    try:
        # Atualiza estoque
        remedio.ESTOQUE = remedio.ESTOQUE - compra.quantidade
        session.add(remedio)

        nova_transacao = Transacao(
            id_cliente=compra.id_cliente,
            id_remedio=compra.id_remedio,
            id_pet=compra.id_pet,
            quantidade=compra.quantidade,
            valor_desconto=compra.valor_desconto or 0,
            valor_frete=compra.valor_frete or 0,
            forma_pagamento=compra.forma_pagamento,
            parcelas=compra.parcelas
        )
        session.add(nova_transacao)
        session.commit()
        session.refresh(nova_transacao)

        return {"mensagem": "Compra registrada com sucesso", "id": nova_transacao.ID}
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
