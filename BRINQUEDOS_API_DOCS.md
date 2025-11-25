# 🧸 API de Brinquedos - Documentação Completa

## 📋 Índice
- [Visão Geral](#visão-geral)
- [Endpoints Disponíveis](#endpoints-disponíveis)
- [Exemplos de Uso](#exemplos-de-uso)
- [Schemas e Validações](#schemas-e-validações)

---

## 🎯 Visão Geral

A API de Brinquedos oferece um CRUD completo e profissional para gerenciar produtos de brinquedos para pets. 

### Categorias Disponíveis:
- **Pelúcia** - Brinquedos macios e fofos
- **Bola** - Brinquedos para jogar e buscar
- **Interativo** - Brinquedos que estimulam a inteligência
- **Mordedor** - Brinquedos para roer e morder

### Funcionalidades:
✅ Listagem com filtros avançados  
✅ Busca por ID ou categoria  
✅ Cadastro com validações  
✅ Atualização completa  
✅ Atualização de estoque  
✅ Exclusão  
✅ Estatísticas e relatórios  

---

## 🚀 Endpoints Disponíveis

### 1. **GET** `/brinquedos/` - Listar todos os brinquedos
Lista todos os brinquedos com filtros opcionais.

**Query Parameters:**
- `categoria` (opcional): Pelúcia | Bola | Interativo | Mordedor
- `min_preco` (opcional): Preço mínimo
- `max_preco` (opcional): Preço máximo
- `em_estoque` (opcional): true/false

**Exemplo de requisição:**
```bash
GET /brinquedos/?categoria=Pelúcia&em_estoque=true
```

**Resposta de sucesso (200):**
```json
{
  "mensagem": "Lista de brinquedos recuperada com sucesso",
  "total": 2,
  "data": [
    {
      "ID": 1,
      "NOME": "Urso de Pelúcia",
      "CATEGORIA": "Pelúcia",
      "PRECO": 49.90,
      "ESTOQUE": 50,
      "IMAGEM": "/imagens/urso-pelucia.png",
      "DESCRICAO": "Brinquedo macio e seguro para pets"
    }
  ]
}
```

---

### 2. **GET** `/brinquedos/{brinquedo_id}` - Buscar por ID
Busca um brinquedo específico pelo ID.

**Exemplo de requisição:**
```bash
GET /brinquedos/1
```

**Resposta de sucesso (200):**
```json
{
  "mensagem": "Brinquedo encontrado",
  "data": {
    "id": 1,
    "nome": "Urso de Pelúcia",
    "categoria": "Pelúcia",
    "preco": 49.90,
    "estoque": 50,
    "imagem": "/imagens/urso-pelucia.png",
    "descricao": "Brinquedo macio e seguro para pets"
  }
}
```

**Resposta de erro (404):**
```json
{
  "detail": "Brinquedo não encontrado"
}
```

---

### 3. **GET** `/brinquedos/categoria/{categoria}` - Listar por categoria
Lista todos os brinquedos de uma categoria específica.

**Exemplo de requisição:**
```bash
GET /brinquedos/categoria/Bola
```

**Resposta de sucesso (200):**
```json
{
  "mensagem": "Brinquedos da categoria Bola",
  "total": 3,
  "data": [
    {
      "id": 2,
      "nome": "Bola Colorida",
      "categoria": "Bola",
      "preco": 19.90,
      "estoque": 100,
      "imagem": "/imagens/bola-colorida.png",
      "descricao": "Bola resistente para brincadeiras"
    }
  ]
}
```

---

### 4. **POST** `/brinquedos/cadastrar` - Cadastrar novo brinquedo
Cadastra um novo brinquedo no sistema.

**Body (JSON):**
```json
{
  "nome": "Urso de Pelúcia",
  "categoria": "Pelúcia",
  "preco": 49.90,
  "estoque": 50,
  "imagem": "/imagens/urso-pelucia.png",
  "descricao": "Brinquedo macio e seguro para pets"
}
```

**Validações:**
- ✅ Nome deve ser único
- ✅ Categoria deve ser: Pelúcia, Bola, Interativo ou Mordedor
- ✅ Preço deve ser maior que 0
- ✅ Estoque deve ser maior ou igual a 0

**Resposta de sucesso (201):**
```json
{
  "mensagem": "Brinquedo 'Urso de Pelúcia' cadastrado com sucesso",
  "id": 1,
  "data": {
    "id": 1,
    "nome": "Urso de Pelúcia",
    "categoria": "Pelúcia",
    "preco": 49.90,
    "estoque": 50,
    "imagem": "/imagens/urso-pelucia.png",
    "descricao": "Brinquedo macio e seguro para pets"
  }
}
```

**Resposta de erro (400):**
```json
{
  "detail": "Já existe um brinquedo cadastrado com o nome 'Urso de Pelúcia'"
}
```

---

### 5. **PUT** `/brinquedos/atualizar/{brinquedo_id}` - Atualizar brinquedo
Atualiza todos os dados de um brinquedo existente.

**Exemplo de requisição:**
```bash
PUT /brinquedos/atualizar/1
```

**Body (JSON):**
```json
{
  "nome": "Urso de Pelúcia Premium",
  "categoria": "Pelúcia",
  "preco": 59.90,
  "estoque": 30,
  "imagem": "/imagens/urso-pelucia-premium.png",
  "descricao": "Versão premium do brinquedo"
}
```

**Resposta de sucesso (200):**
```json
{
  "mensagem": "Brinquedo atualizado com sucesso",
  "id": 1,
  "data": {
    "id": 1,
    "nome": "Urso de Pelúcia Premium",
    "categoria": "Pelúcia",
    "preco": 59.90,
    "estoque": 30,
    "imagem": "/imagens/urso-pelucia-premium.png",
    "descricao": "Versão premium do brinquedo"
  }
}
```

---

### 6. **PATCH** `/brinquedos/estoque/{brinquedo_id}` - Atualizar estoque
Atualiza apenas o estoque de um brinquedo (útil para reposições).

**Query Parameter:**
- `quantidade` (obrigatório): Nova quantidade em estoque

**Exemplo de requisição:**
```bash
PATCH /brinquedos/estoque/1?quantidade=100
```

**Resposta de sucesso (200):**
```json
{
  "mensagem": "Estoque atualizado com sucesso",
  "brinquedo": "Urso de Pelúcia",
  "estoque_anterior": 50,
  "estoque_atual": 100,
  "diferenca": 50
}
```

---

### 7. **DELETE** `/brinquedos/deletar/{brinquedo_id}` - Deletar brinquedo
Remove um brinquedo do sistema.

⚠️ **ATENÇÃO:** Esta ação é irreversível!

**Exemplo de requisição:**
```bash
DELETE /brinquedos/deletar/1
```

**Resposta de sucesso (200):**
```json
{
  "mensagem": "Brinquedo 'Urso de Pelúcia' deletado com sucesso",
  "id": 1
}
```

**Resposta de erro (404):**
```json
{
  "detail": "Brinquedo não encontrado"
}
```

---

### 8. **GET** `/brinquedos/estatisticas/resumo` - Estatísticas gerais
Retorna estatísticas completas sobre os brinquedos cadastrados.

**Exemplo de requisição:**
```bash
GET /brinquedos/estatisticas/resumo
```

**Resposta de sucesso (200):**
```json
{
  "mensagem": "Estatísticas recuperadas com sucesso",
  "estatisticas": {
    "total_brinquedos": 10,
    "total_unidades_estoque": 450,
    "valor_total_estoque": 8975.50,
    "produtos_por_categoria": {
      "Pelúcia": 3,
      "Bola": 4,
      "Interativo": 2,
      "Mordedor": 1
    },
    "produtos_em_falta": {
      "quantidade": 2,
      "lista": ["Bola Tênis", "Mordedor Grande"]
    }
  }
}
```

---

## 📝 Schemas e Validações

### BrinquedoSchema

```python
{
  "nome": str,           # Obrigatório, 1-100 caracteres
  "categoria": str,      # Obrigatório, valores: "Pelúcia" | "Bola" | "Interativo" | "Mordedor"
  "preco": float,        # Obrigatório, maior que 0
  "estoque": int,        # Obrigatório, maior ou igual a 0
  "imagem": str | null,  # Opcional, URL da imagem
  "descricao": str | null # Opcional, máximo 500 caracteres
}
```

### Validações Automáticas:
- ✅ Nome único no sistema
- ✅ Categoria deve ser uma das 4 opções válidas
- ✅ Preço sempre positivo
- ✅ Estoque nunca negativo
- ✅ Descrição limitada a 500 caracteres

---

## 🎨 Integração com Frontend

### Exemplo de uso no React/TypeScript:

```typescript
// Buscar todos os brinquedos de uma categoria
const fetchBrinquedosPorCategoria = async (categoria: string) => {
  const response = await fetch(`http://localhost:8000/brinquedos/categoria/${categoria}`);
  const data = await response.json();
  return data.data;
};

// Cadastrar novo brinquedo
const criarBrinquedo = async (brinquedo: BrinquedoSchema) => {
  const response = await fetch('http://localhost:8000/brinquedos/cadastrar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(brinquedo)
  });
  return await response.json();
};

// Atualizar estoque
const atualizarEstoque = async (id: number, quantidade: number) => {
  const response = await fetch(
    `http://localhost:8000/brinquedos/estoque/${id}?quantidade=${quantidade}`,
    { method: 'PATCH' }
  );
  return await response.json();
};
```

---

## 🔧 Testando a API

### Com cURL:

```bash
# Listar todos os brinquedos
curl -X GET "http://localhost:8000/brinquedos/"

# Cadastrar novo brinquedo
curl -X POST "http://localhost:8000/brinquedos/cadastrar" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Urso de Pelúcia",
    "categoria": "Pelúcia",
    "preco": 49.90,
    "estoque": 50,
    "imagem": "/imagens/urso-pelucia.png",
    "descricao": "Brinquedo macio e seguro"
  }'

# Atualizar estoque
curl -X PATCH "http://localhost:8000/brinquedos/estoque/1?quantidade=100"

# Deletar brinquedo
curl -X DELETE "http://localhost:8000/brinquedos/deletar/1"
```

---

## 📊 Estrutura do Banco de Dados

### Tabela: `brinquedos`

| Campo      | Tipo    | Nullable | Unique | Default |
|------------|---------|----------|--------|---------|
| ID         | Integer | No       | Yes    | Auto    |
| NOME       | String  | No       | Yes    | -       |
| CATEGORIA  | String  | No       | No     | -       |
| PRECO      | Float   | No       | No     | 0.0     |
| ESTOQUE    | Integer | No       | No     | 0       |
| IMAGEM     | String  | Yes      | No     | null    |
| DESCRICAO  | String  | Yes      | No     | null    |

---

## 🎯 Boas Práticas

1. **Sempre valide os dados no frontend** antes de enviar para a API
2. **Use filtros** para otimizar as buscas (categoria, preço, estoque)
3. **Implemente paginação** para listas grandes
4. **Cache de imagens** no frontend para melhor performance
5. **Trate erros** adequadamente (404, 400, 500)
6. **Use PATCH** para atualizar apenas o estoque
7. **Verifique estatísticas** regularmente para gestão de estoque

---

## 🚀 Próximos Passos

- [ ] Adicionar endpoint de busca por nome
- [ ] Implementar paginação
- [ ] Adicionar sistema de avaliações
- [ ] Integrar com sistema de compras
- [ ] Adicionar upload de imagens
- [ ] Implementar cache com Redis

---

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação interativa em:
`http://localhost:8000/docs`

---

**Desenvolvido com ❤️ para FarmPet**
