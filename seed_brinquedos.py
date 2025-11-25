"""
Script para popular o banco de dados com brinquedos de exemplo
Execute: python seed_brinquedos.py
"""
from models import SessionLocal, Brinquedo

def seed_brinquedos():
    session = SessionLocal()
    
    brinquedos_exemplo = [
        {
            "nome": "Urso de Pelúcia",
            "categoria": "Pelúcia",
            "preco": 49.90,
            "estoque": 50,
            "imagem": "/imagens/urso-pelucia.png",
            "descricao": "Brinquedo macio e seguro para pets de todos os portes"
        },
        {
            "nome": "Bola Colorida",
            "categoria": "Bola",
            "preco": 19.90,
            "estoque": 100,
            "imagem": "/imagens/bola-colorida.png",
            "descricao": "Bola resistente e colorida para brincadeiras ao ar livre"
        },
        {
            "nome": "Brinquedo Interativo Puzzle",
            "categoria": "Interativo",
            "preco": 89.90,
            "estoque": 30,
            "imagem": "/imagens/puzzle-interativo.png",
            "descricao": "Estimula a inteligência do seu pet com desafios divertidos"
        },
        {
            "nome": "Mordedor de Borracha",
            "categoria": "Mordedor",
            "preco": 29.90,
            "estoque": 75,
            "imagem": "/imagens/mordedor-borracha.png",
            "descricao": "Mordedor resistente para cães que adoram roer"
        },
        {
            "nome": "Pelúcia Patinho",
            "categoria": "Pelúcia",
            "preco": 39.90,
            "estoque": 40,
            "imagem": "/imagens/patinho-pelucia.png",
            "descricao": "Patinho fofo com som de apito interno"
        },
        {
            "nome": "Bola de Tênis",
            "categoria": "Bola",
            "preco": 15.90,
            "estoque": 120,
            "imagem": "/imagens/bola-tenis.png",
            "descricao": "Bola de tênis especial para pets, tamanho padrão"
        },
        {
            "nome": "Corda Interativa",
            "categoria": "Interativo",
            "preco": 24.90,
            "estoque": 60,
            "imagem": "/imagens/corda-interativa.png",
            "descricao": "Corda com nós para brincadeiras de puxar"
        },
        {
            "nome": "Osso de Nylon",
            "categoria": "Mordedor",
            "preco": 34.90,
            "estoque": 80,
            "imagem": "/imagens/osso-nylon.png",
            "descricao": "Osso de nylon durável com sabor de bacon"
        },
        {
            "nome": "Coelho de Pelúcia",
            "categoria": "Pelúcia",
            "preco": 44.90,
            "estoque": 35,
            "imagem": "/imagens/coelho-pelucia.png",
            "descricao": "Coelho de pelúcia macio com orelhas longas"
        },
        {
            "nome": "Bola com Luz LED",
            "categoria": "Bola",
            "preco": 39.90,
            "estoque": 45,
            "imagem": "/imagens/bola-led.png",
            "descricao": "Bola que acende ao tocar, perfeita para brincadeiras noturnas"
        }
    ]
    
    try:
        count = 0
        for item in brinquedos_exemplo:
            # Verifica se já existe
            existente = session.query(Brinquedo).filter(Brinquedo.NOME == item["nome"]).first()
            if existente:
                print(f"❌ '{item['nome']}' já existe no banco")
                continue
            
            # Cria novo brinquedo
            brinquedo = Brinquedo(
                nome=item["nome"],
                categoria=item["categoria"],
                preco=item["preco"],
                estoque=item["estoque"],
                imagem=item["imagem"],
                descricao=item["descricao"]
            )
            session.add(brinquedo)
            count += 1
            print(f"✅ '{item['nome']}' adicionado com sucesso")
        
        session.commit()
        print(f"\n🎉 {count} brinquedos cadastrados com sucesso!")
        
        # Mostra estatísticas
        total = session.query(Brinquedo).count()
        print(f"\n📊 Total de brinquedos no banco: {total}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao popular banco: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    print("🚀 Populando banco de dados com brinquedos de exemplo...\n")
    seed_brinquedos()
