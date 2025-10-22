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

@pet_router.post("/Cadastrar_pet")
async def criar_pet(petschemas: Petschema, session: Session = Depends(pegar_sessao)):
    existente = session.query(Pet).filter(Pet.NOME_PET == petschemas.nome, Pet.CLIENTE_ID == petschemas.id_cliente).first()
    if existente:
        raise HTTPException(status_code=400, detail="Pet já cadastrado no sistema para este cliente")
    try:
        novo_pet = Pet(petschemas.nome, petschemas.especie, petschemas.raca, petschemas.endereco_dono, petschemas.id_cliente)
        session.add(novo_pet)
        session.commit()
        session.refresh(novo_pet)  # Garante que ID está disponível
        return {"mensagem": f"Pet cadastrado com sucesso: {novo_pet.NOME_PET}", "id": novo_pet.ID}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))