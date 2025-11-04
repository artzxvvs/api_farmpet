# ...existing code...
from fastapi import APIRouter, Depends, HTTPException
from models import Pet, db
from dependencies import pegar_sessao
# from main import bcrypt_context  # removido: não usado
from schemas import Petschema
from sqlalchemy.orm import Session
from sqlalchemy import select
import pandas as pd

pet_router = APIRouter(prefix="/pets", tags=["Pets"])

@pet_router.get("/")
async def listar_pets():
    conn = db.connect()
    with conn as con:
        query = select(Pet)
        result = pd.read_sql(query, con)
        result = result.to_dict(orient='records')

    """
    Essa é a rota para listar todos os pets
    """
    return {"mensagem": "Lista de pets acessada com sucesso!", "data": result}

@pet_router.post("/Cadastrar_pet", status_code=201)
async def criar_pet(petschemas: Petschema, session: Session = Depends(pegar_sessao)):
    # Usar nomes de coluna do modelo: NOME e ID_CLIENTE
    existente = session.query(Pet).filter(Pet.NOME == petschemas.nome, Pet.ID_CLIENTE == petschemas.id_cliente).first()
    if existente:
        raise HTTPException(status_code=400, detail="Pet já cadastrado no sistema para este cliente")
    try:
        # O modelo Pet atualmente só define NOME e ID_CLIENTE.
        # Atribuímos explicitamente para evitar depender de um __init__ inexistente.
        novo_pet = Pet()
        novo_pet.NOME = petschemas.nome
        novo_pet.ID_CLIENTE = petschemas.id_cliente
        # campos opcionais no schema (especie, raca, idade, endereco_dono) não são
        # persistidos porque não existem colunas correspondentes no modelo.
        session.add(novo_pet)
        session.commit()
        session.refresh(novo_pet)  # Garante que ID está disponível
        return {"mensagem": f"Pet cadastrado com sucesso: {novo_pet.NOME}", "id": novo_pet.ID}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))