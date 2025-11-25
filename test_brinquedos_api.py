"""
Script para testar todas as funcionalidades da API de Brinquedos
Execute: python test_brinquedos_api.py
ATENÇÃO: Inicie o servidor antes (uvicorn main:app --reload)
"""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_response(title: str, response: requests.Response):
    """Formata e imprime a resposta da API"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTE: {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print(f"{'='*60}\n")


def test_listar_todos():
    """Testa listagem de todos os brinquedos"""
    response = requests.get(f"{BASE_URL}/brinquedos/")
    print_response("Listar Todos os Brinquedos", response)
    return response.status_code == 200


def test_filtros():
    """Testa filtros de listagem"""
    # Filtro por categoria
    response = requests.get(f"{BASE_URL}/brinquedos/?categoria=Pelúcia")
    print_response("Filtrar por Categoria (Pelúcia)", response)
    
    # Filtro por preço
    response = requests.get(f"{BASE_URL}/brinquedos/?min_preco=20&max_preco=50")
    print_response("Filtrar por Preço (R$ 20 - R$ 50)", response)
    
    # Filtro por estoque
    response = requests.get(f"{BASE_URL}/brinquedos/?em_estoque=true")
    print_response("Filtrar Apenas em Estoque", response)


def test_buscar_por_id():
    """Testa busca por ID"""
    response = requests.get(f"{BASE_URL}/brinquedos/1")
    print_response("Buscar Brinquedo por ID (1)", response)
    return response.status_code == 200


def test_buscar_por_categoria():
    """Testa busca por categoria"""
    response = requests.get(f"{BASE_URL}/brinquedos/categoria/Bola")
    print_response("Buscar por Categoria (Bola)", response)
    return response.status_code == 200


def test_criar_brinquedo():
    """Testa criação de novo brinquedo"""
    novo_brinquedo = {
        "nome": "Brinquedo de Teste",
        "categoria": "Interativo",
        "preco": 99.90,
        "estoque": 25,
        "imagem": "/imagens/teste.png",
        "descricao": "Brinquedo criado para teste da API"
    }
    
    response = requests.post(
        f"{BASE_URL}/brinquedos/cadastrar",
        json=novo_brinquedo
    )
    print_response("Criar Novo Brinquedo", response)
    
    if response.status_code == 201:
        return response.json().get("id")
    return None


def test_criar_duplicado():
    """Testa criação de brinquedo duplicado (deve falhar)"""
    brinquedo_duplicado = {
        "nome": "Urso de Pelúcia",  # Já existe
        "categoria": "Pelúcia",
        "preco": 49.90,
        "estoque": 50
    }
    
    response = requests.post(
        f"{BASE_URL}/brinquedos/cadastrar",
        json=brinquedo_duplicado
    )
    print_response("Criar Brinquedo Duplicado (deve falhar)", response)
    return response.status_code == 400


def test_atualizar_brinquedo(brinquedo_id: int):
    """Testa atualização de brinquedo"""
    if not brinquedo_id:
        print("⚠️ Pulando teste de atualização (ID não disponível)")
        return False
    
    brinquedo_atualizado = {
        "nome": "Brinquedo de Teste Atualizado",
        "categoria": "Interativo",
        "preco": 109.90,
        "estoque": 15,
        "imagem": "/imagens/teste-atualizado.png",
        "descricao": "Brinquedo atualizado via teste da API"
    }
    
    response = requests.put(
        f"{BASE_URL}/brinquedos/atualizar/{brinquedo_id}",
        json=brinquedo_atualizado
    )
    print_response(f"Atualizar Brinquedo (ID: {brinquedo_id})", response)
    return response.status_code == 200


def test_atualizar_estoque(brinquedo_id: int):
    """Testa atualização de estoque"""
    if not brinquedo_id:
        print("⚠️ Pulando teste de atualização de estoque (ID não disponível)")
        return False
    
    response = requests.patch(
        f"{BASE_URL}/brinquedos/estoque/{brinquedo_id}?quantidade=50"
    )
    print_response(f"Atualizar Estoque (ID: {brinquedo_id})", response)
    return response.status_code == 200


def test_estatisticas():
    """Testa endpoint de estatísticas"""
    response = requests.get(f"{BASE_URL}/brinquedos/estatisticas/resumo")
    print_response("Estatísticas Gerais", response)
    return response.status_code == 200


def test_deletar_brinquedo(brinquedo_id: int):
    """Testa exclusão de brinquedo"""
    if not brinquedo_id:
        print("⚠️ Pulando teste de exclusão (ID não disponível)")
        return False
    
    response = requests.delete(f"{BASE_URL}/brinquedos/deletar/{brinquedo_id}")
    print_response(f"Deletar Brinquedo (ID: {brinquedo_id})", response)
    return response.status_code == 200


def test_validacoes():
    """Testa validações da API"""
    print(f"\n{'='*60}")
    print("🔍 TESTANDO VALIDAÇÕES")
    print(f"{'='*60}\n")
    
    # Preço inválido
    response = requests.post(
        f"{BASE_URL}/brinquedos/cadastrar",
        json={
            "nome": "Teste Preço Inválido",
            "categoria": "Bola",
            "preco": -10,  # Preço negativo
            "estoque": 10
        }
    )
    print_response("Validação: Preço Negativo (deve falhar)", response)
    
    # Categoria inválida
    response = requests.post(
        f"{BASE_URL}/brinquedos/cadastrar",
        json={
            "nome": "Teste Categoria Inválida",
            "categoria": "CategoriaInexistente",
            "preco": 10,
            "estoque": 10
        }
    )
    print_response("Validação: Categoria Inválida (deve falhar)", response)


def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "🚀" * 30)
    print("   INICIANDO TESTES DA API DE BRINQUEDOS")
    print("🚀" * 30 + "\n")
    
    resultados = []
    brinquedo_test_id = None
    
    try:
        # Testes de leitura
        resultados.append(("Listar Todos", test_listar_todos()))
        test_filtros()
        resultados.append(("Buscar por ID", test_buscar_por_id()))
        resultados.append(("Buscar por Categoria", test_buscar_por_categoria()))
        
        # Testes de criação
        brinquedo_test_id = test_criar_brinquedo()
        resultados.append(("Criar Brinquedo", brinquedo_test_id is not None))
        resultados.append(("Criar Duplicado", test_criar_duplicado()))
        
        # Testes de atualização
        resultados.append(("Atualizar Brinquedo", test_atualizar_brinquedo(brinquedo_test_id)))
        resultados.append(("Atualizar Estoque", test_atualizar_estoque(brinquedo_test_id)))
        
        # Testes de estatísticas
        resultados.append(("Estatísticas", test_estatisticas()))
        
        # Testes de validação
        test_validacoes()
        
        # Teste de exclusão (por último)
        resultados.append(("Deletar Brinquedo", test_deletar_brinquedo(brinquedo_test_id)))
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar ao servidor!")
        print("💡 Certifique-se de que o servidor está rodando:")
        print("   uvicorn main:app --reload\n")
        return
    
    # Resumo dos testes
    print("\n" + "📊" * 30)
    print("   RESUMO DOS TESTES")
    print("📊" * 30 + "\n")
    
    total = len(resultados)
    passou = sum(1 for _, resultado in resultados if resultado)
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status} - {nome}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passou}/{total} testes passaram")
    print(f"Taxa de sucesso: {(passou/total)*100:.1f}%")
    print(f"{'='*60}\n")
    
    if passou == total:
        print("🎉 TODOS OS TESTES PASSARAM! 🎉\n")
    else:
        print("⚠️ Alguns testes falharam. Verifique os detalhes acima.\n")


if __name__ == "__main__":
    run_all_tests()
