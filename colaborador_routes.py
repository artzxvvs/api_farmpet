
from fastapi import APIRouter, Depends, HTTPException
from models import Colaborador, db
from dependencies import pegar_sessao
from security import bcrypt_context
from schemas import Colaboradorchema
from sqlalchemy.orm import Session
from sqlalchemy import select
import pandas as pd
from sqlalchemy.exc import IntegrityError
colaborador_router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])

@colaborador_router.get("/")
async def listar_colaboradores():
    conn = db.connect()
    with conn as con:
        query = select(Colaborador)
        result = pd.read_sql(query, con)
        result = result.to_dict(orient='records')

    """
    Essa é a rota para listar todos os colaboradores
    """
    return {"mensagem": "Lista de colaboradores acessada com sucesso!", "data": result}


@colaborador_router.post("/Cadastrar_Colaborador", status_code=201)
async def criar_colaborador(colaborador: Colaboradorchema, session: Session = Depends(pegar_sessao)):
    # Normaliza CPF (remove pontuação) e trim nos campos
    cpf_recebido = (colaborador.cpf or "").strip()
    cpf_normalizado = "".join(ch for ch in cpf_recebido if ch.isdigit())
    telefone_normalizado = (colaborador.telefone or "").strip()

    # Validação rápida de CPF (espera 11 dígitos)
    if cpf_normalizado and len(cpf_normalizado) != 11:
        raise HTTPException(status_code=400, detail="CPF inválido: deve conter 11 dígitos")

    # debug: log do CPF e telefone recebidos
    print(f"[DEBUG] CPF recebido: {cpf_recebido} -> normalizado: {cpf_normalizado}")
    print(f"[DEBUG] Telefone recebido: {telefone_normalizado}")

    existente = session.query(Colaborador).filter(Colaborador.CPF == cpf_normalizado).first()
    if existente:
        raise HTTPException(status_code=400, detail=f"CPF já cadastrado no sistema: {existente.CPF}")

    try:
        # Cria novo colaborador usando a ordem clara (nome, cpf, telefone, cargo)
        novo_colaborador = Colaborador(
            nome=colaborador.nome,
            cpf=cpf_normalizado,
            telefone=telefone_normalizado,
            cargo=colaborador.cargo
        )
        session.add(novo_colaborador)
        session.commit()
        session.refresh(novo_colaborador)  # Garante que ID está disponível
        return {"mensagem": f"Colaborador cadastrado com sucesso: {novo_colaborador.NOME}", "id": novo_colaborador.ID}
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@colaborador_router.put("/atualizar_colaborador/{colaborador_id}")
async def atualizar_colaborador(colaborador_id: int, colaborador: Colaboradorchema, session: Session = Depends(pegar_sessao)):
    """
    Atualiza os dados de um colaborador existente
    """
    colab_existente = session.query(Colaborador).filter(Colaborador.ID == colaborador_id).first()
    if not colab_existente:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    
    # Normaliza CPF
    cpf_normalizado = "".join(ch for ch in (colaborador.cpf or "").strip() if ch.isdigit())
    
    # Verifica se CPF já está sendo usado por outro colaborador
    if cpf_normalizado and cpf_normalizado != colab_existente.CPF:
        cpf_existe = session.query(Colaborador).filter(Colaborador.CPF == cpf_normalizado).first()
        if cpf_existe:
            raise HTTPException(status_code=400, detail="CPF já está sendo usado por outro colaborador")
    
    try:
        colab_existente.NOME = colaborador.nome
        colab_existente.CPF = cpf_normalizado
        colab_existente.TELEFONE = (colaborador.telefone or "").strip()
        colab_existente.CARGO = colaborador.cargo
        
        session.commit()
        session.refresh(colab_existente)
        return {"mensagem": "Colaborador atualizado com sucesso", "id": colab_existente.ID}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar colaborador: {str(e)}")


@colaborador_router.delete("/deletar_colaborador/{colaborador_id}")
async def deletar_colaborador(colaborador_id: int, session: Session = Depends(pegar_sessao)):
    """
    Deleta um colaborador do sistema
    """
    colaborador = session.query(Colaborador).filter(Colaborador.ID == colaborador_id).first()
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    
    try:
        session.delete(colaborador)
        session.commit()
        return {"mensagem": "Colaborador deletado com sucesso", "id": colaborador_id}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar colaborador: {str(e)}")