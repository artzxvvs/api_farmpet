from fastapi import APIRouter, Depends, HTTPException, Query
from models import Brinquedo, db
from dependencies import pegar_sessao
from schemas import BrinquedoSchema, CategoriaBrinquedo
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
import pandas as pd

brinquedo_router = APIRouter(prefix="/brinquedos", tags=["Brinquedos"])


@brinquedo_router.get("/", summary="Listar todos os brinquedos")
async def listar_brinquedos(
    categoria: Optional[CategoriaBrinquedo] = Query(None, description="Filtrar por categoria"),
    min_preco: Optional[float] = Query(None, ge=0, description="Preço mínimo"),
    max_preco: Optional[float] = Query(None, ge=0, description="Preço máximo"),
    em_estoque: Optional[bool] = Query(None, description="Apenas produtos em estoque")
):
    """
    Lista todos os brinquedos disponíveis com filtros opcionais.
    
    **Filtros disponíveis:**
    - `categoria`: Pelúcia, Bola, Interativo, Mordedor
    - `min_preco`: Preço mínimo
    - `max_preco`: Preço máximo
    - `em_estoque`: true para mostrar apenas itens com estoque
    """
    conn = db.connect()
    with conn as con:
        query = select(Brinquedo)
        result = pd.read_sql(query, con)
        
        # Aplicar filtros
        if categoria:
            result = result[result['CATEGORIA'] == categoria]
        if min_preco is not None:
            result = result[result['PRECO'] >= min_preco]
        if max_preco is not None:
            result = result[result['PRECO'] <= max_preco]
        if em_estoque:
            result = result[result['ESTOQUE'] > 0]
        
        result = result.to_dict(orient='records')

    return {
        "mensagem": "Lista de brinquedos recuperada com sucesso",
        "total": len(result),
        "data": result
    }


@brinquedo_router.get("/{brinquedo_id}", summary="Buscar brinquedo por ID")
async def buscar_brinquedo(brinquedo_id: int, session: Session = Depends(pegar_sessao)):
    """
    Busca um brinquedo específico pelo ID.
    """
    brinquedo = session.query(Brinquedo).filter(Brinquedo.ID == brinquedo_id).first()
    if not brinquedo:
        raise HTTPException(status_code=404, detail="Brinquedo não encontrado")
    
    return {
        "mensagem": "Brinquedo encontrado",
        "data": {
            "id": brinquedo.ID,
            "nome": brinquedo.NOME,
            "categoria": brinquedo.CATEGORIA,
            "preco": brinquedo.PRECO,
            "estoque": brinquedo.ESTOQUE,
            "imagem": brinquedo.IMAGEM,
            "descricao": brinquedo.DESCRICAO
        }
    }


@brinquedo_router.get("/categoria/{categoria}", summary="Listar brinquedos por categoria")
async def listar_por_categoria(categoria: CategoriaBrinquedo, session: Session = Depends(pegar_sessao)):
    """
    Lista todos os brinquedos de uma categoria específica.
    
    **Categorias disponíveis:** Pelúcia, Bola, Interativo, Mordedor
    """
    brinquedos = session.query(Brinquedo).filter(Brinquedo.CATEGORIA == categoria).all()
    
    return {
        "mensagem": f"Brinquedos da categoria {categoria}",
        "total": len(brinquedos),
        "data": [{
            "id": b.ID,
            "nome": b.NOME,
            "categoria": b.CATEGORIA,
            "preco": b.PRECO,
            "estoque": b.ESTOQUE,
            "imagem": b.IMAGEM,
            "descricao": b.DESCRICAO
        } for b in brinquedos]
    }


@brinquedo_router.post("/cadastrar", status_code=201, summary="Cadastrar novo brinquedo")
async def criar_brinquedo(brinquedo: BrinquedoSchema, session: Session = Depends(pegar_sessao)):
    """
    Cadastra um novo brinquedo no sistema.
    
    **Campos obrigatórios:**
    - nome: Nome do brinquedo (único)
    - categoria: Pelúcia, Bola, Interativo, Mordedor
    - preco: Preço do produto (maior que 0)
    - estoque: Quantidade em estoque (maior ou igual a 0)
    
    **Campos opcionais:**
    - imagem: URL da imagem do produto
    - descricao: Descrição detalhada do produto
    """
    # Verifica se já existe um brinquedo com esse nome
    existente = session.query(Brinquedo).filter(Brinquedo.NOME == brinquedo.nome).first()
    if existente:
        raise HTTPException(
            status_code=400, 
            detail=f"Já existe um brinquedo cadastrado com o nome '{brinquedo.nome}'"
        )
    
    # Valida categoria
    categorias_validas = ["Pelúcia", "Bola", "Interativo", "Mordedor"]
    if brinquedo.categoria not in categorias_validas:
        raise HTTPException(
            status_code=400,
            detail=f"Categoria inválida. Categorias aceitas: {', '.join(categorias_validas)}"
        )
    
    try:
        novo_brinquedo = Brinquedo(
            nome=brinquedo.nome,
            categoria=brinquedo.categoria,
            preco=brinquedo.preco,
            estoque=brinquedo.estoque,
            imagem=brinquedo.imagem,
            descricao=brinquedo.descricao
        )
        session.add(novo_brinquedo)
        session.commit()
        session.refresh(novo_brinquedo)
        
        return {
            "mensagem": f"Brinquedo '{novo_brinquedo.NOME}' cadastrado com sucesso",
            "id": novo_brinquedo.ID,
            "data": {
                "id": novo_brinquedo.ID,
                "nome": novo_brinquedo.NOME,
                "categoria": novo_brinquedo.CATEGORIA,
                "preco": novo_brinquedo.PRECO,
                "estoque": novo_brinquedo.ESTOQUE,
                "imagem": novo_brinquedo.IMAGEM,
                "descricao": novo_brinquedo.DESCRICAO
            }
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar brinquedo: {str(e)}")


@brinquedo_router.put("/atualizar/{brinquedo_id}", summary="Atualizar brinquedo")
async def atualizar_brinquedo(
    brinquedo_id: int, 
    brinquedo: BrinquedoSchema, 
    session: Session = Depends(pegar_sessao)
):
    """
    Atualiza os dados de um brinquedo existente.
    
    **Parâmetros:**
    - brinquedo_id: ID do brinquedo a ser atualizado
    - Todos os campos do BrinquedoSchema
    
    **Validações:**
    - Verifica se o brinquedo existe
    - Valida se o novo nome não está sendo usado por outro brinquedo
    - Valida categoria
    """
    brinquedo_existente = session.query(Brinquedo).filter(Brinquedo.ID == brinquedo_id).first()
    if not brinquedo_existente:
        raise HTTPException(status_code=404, detail="Brinquedo não encontrado")
    
    # Verifica se o nome já está sendo usado por outro brinquedo
    if brinquedo.nome != brinquedo_existente.NOME:
        nome_existe = session.query(Brinquedo).filter(
            Brinquedo.NOME == brinquedo.nome,
            Brinquedo.ID != brinquedo_id
        ).first()
        if nome_existe:
            raise HTTPException(
                status_code=400, 
                detail=f"Já existe outro brinquedo com o nome '{brinquedo.nome}'"
            )
    
    # Valida categoria
    categorias_validas = ["Pelúcia", "Bola", "Interativo", "Mordedor"]
    if brinquedo.categoria not in categorias_validas:
        raise HTTPException(
            status_code=400,
            detail=f"Categoria inválida. Categorias aceitas: {', '.join(categorias_validas)}"
        )
    
    try:
        brinquedo_existente.NOME = brinquedo.nome
        brinquedo_existente.CATEGORIA = brinquedo.categoria
        brinquedo_existente.PRECO = brinquedo.preco
        brinquedo_existente.ESTOQUE = brinquedo.estoque
        brinquedo_existente.IMAGEM = brinquedo.imagem
        brinquedo_existente.DESCRICAO = brinquedo.descricao
        
        session.commit()
        session.refresh(brinquedo_existente)
        
        return {
            "mensagem": "Brinquedo atualizado com sucesso",
            "id": brinquedo_existente.ID,
            "data": {
                "id": brinquedo_existente.ID,
                "nome": brinquedo_existente.NOME,
                "categoria": brinquedo_existente.CATEGORIA,
                "preco": brinquedo_existente.PRECO,
                "estoque": brinquedo_existente.ESTOQUE,
                "imagem": brinquedo_existente.IMAGEM,
                "descricao": brinquedo_existente.DESCRICAO
            }
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar brinquedo: {str(e)}")


@brinquedo_router.patch("/estoque/{brinquedo_id}", summary="Atualizar estoque")
async def atualizar_estoque(
    brinquedo_id: int,
    quantidade: int = Query(..., description="Nova quantidade em estoque"),
    session: Session = Depends(pegar_sessao)
):
    """
    Atualiza apenas o estoque de um brinquedo.
    
    **Útil para:**
    - Reposição de estoque
    - Ajustes de inventário
    - Correções
    """
    brinquedo = session.query(Brinquedo).filter(Brinquedo.ID == brinquedo_id).first()
    if not brinquedo:
        raise HTTPException(status_code=404, detail="Brinquedo não encontrado")
    
    if quantidade < 0:
        raise HTTPException(status_code=400, detail="Quantidade não pode ser negativa")
    
    try:
        estoque_anterior = brinquedo.ESTOQUE
        brinquedo.ESTOQUE = quantidade
        session.commit()
        session.refresh(brinquedo)
        
        return {
            "mensagem": "Estoque atualizado com sucesso",
            "brinquedo": brinquedo.NOME,
            "estoque_anterior": estoque_anterior,
            "estoque_atual": brinquedo.ESTOQUE,
            "diferenca": quantidade - estoque_anterior
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar estoque: {str(e)}")


@brinquedo_router.delete("/deletar/{brinquedo_id}", summary="Deletar brinquedo")
async def deletar_brinquedo(brinquedo_id: int, session: Session = Depends(pegar_sessao)):
    """
    Remove um brinquedo do sistema.
    
    **Atenção:** Esta ação é irreversível!
    
    **Parâmetros:**
    - brinquedo_id: ID do brinquedo a ser deletado
    """
    brinquedo = session.query(Brinquedo).filter(Brinquedo.ID == brinquedo_id).first()
    if not brinquedo:
        raise HTTPException(status_code=404, detail="Brinquedo não encontrado")
    
    try:
        nome_deletado = brinquedo.NOME
        session.delete(brinquedo)
        session.commit()
        
        return {
            "mensagem": f"Brinquedo '{nome_deletado}' deletado com sucesso",
            "id": brinquedo_id
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar brinquedo: {str(e)}")


@brinquedo_router.get("/estatisticas/resumo", summary="Estatísticas gerais")
async def estatisticas_brinquedos(session: Session = Depends(pegar_sessao)):
    """
    Retorna estatísticas gerais sobre os brinquedos cadastrados.
    
    **Informações fornecidas:**
    - Total de brinquedos cadastrados
    - Total em estoque
    - Valor total do estoque
    - Produtos por categoria
    - Produtos em falta (estoque = 0)
    """
    brinquedos = session.query(Brinquedo).all()
    
    total_brinquedos = len(brinquedos)
    total_estoque = sum(b.ESTOQUE for b in brinquedos)
    valor_total_estoque = sum(b.PRECO * b.ESTOQUE for b in brinquedos)
    
    # Contar por categoria
    categorias = {}
    for b in brinquedos:
        categorias[b.CATEGORIA] = categorias.get(b.CATEGORIA, 0) + 1
    
    # Produtos em falta
    produtos_em_falta = [b.NOME for b in brinquedos if b.ESTOQUE == 0]
    
    return {
        "mensagem": "Estatísticas recuperadas com sucesso",
        "estatisticas": {
            "total_brinquedos": total_brinquedos,
            "total_unidades_estoque": total_estoque,
            "valor_total_estoque": round(valor_total_estoque, 2),
            "produtos_por_categoria": categorias,
            "produtos_em_falta": {
                "quantidade": len(produtos_em_falta),
                "lista": produtos_em_falta
            }
        }
    }
