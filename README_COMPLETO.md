# 🎯 FarmPet API - Sistema Completo de Gerenciamento

## 📋 Visão Geral

API REST profissional e completa para gerenciamento de Pet Shop, desenvolvida com **FastAPI**, **SQLAlchemy** e **SQLite/PostgreSQL**.

### ✨ Funcionalidades Principais

- 🔐 **Autenticação e Usuários** - Sistema completo de login e gestão de usuários
- 👥 **Clientes** - Cadastro e gerenciamento de clientes  
- 🐾 **Pets** - Registro de pets dos clientes
- 💊 **Remédios** - Controle de medicamentos veterinários
- 🧸 **Brinquedos** - Gestão completa de brinquedos para pets (NOVO!)
- 👨‍⚕️ **Colaboradores** - Gestão de funcionários
- 🛒 **Compras/Transações** - Sistema de vendas com controle de estoque

---

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/artzxvvs/api_farmpet.git
cd api_farmpet
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**

Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

Windows (CMD):
```cmd
venv\Scripts\activate.bat
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente** (opcional)

Crie um arquivo `.env`:
```env
DATABASE_URL=sqlite:///./farmpet.db
SECRET_KEY=sua_chave_secreta_aqui
```

6. **Crie as tabelas do banco de dados**
```bash
python create_tables.py
```

7. **Popule o banco com dados de exemplo** (opcional)
```bash
python seed_brinquedos.py
```

8. **Inicie o servidor**
```bash
uvicorn main:app --reload
```

9. **Acesse a documentação interativa**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📚 Estrutura do Projeto

```
api_farmpet/
├── alembic/                    # Migrações do banco de dados
├── venv/                       # Ambiente virtual Python
├── main.py                     # Arquivo principal da aplicação
├── models.py                   # Modelos do banco de dados (SQLAlchemy)
├── schemas.py                  # Schemas de validação (Pydantic)
├── security.py                 # Funções de segurança e criptografia
├── dependencies.py             # Dependências e injeção de dependências
├── auth_routes.py             # Rotas de autenticação
├── cliente_routes.py          # Rotas de clientes
├── pet_routes.py              # Rotas de pets
├── remedio_routes.py          # Rotas de remédios
├── brinquedo_routes.py        # Rotas de brinquedos ✨ NOVO
├── colaborador_routes.py      # Rotas de colaboradores
├── compra_routes.py           # Rotas de compras/transações
├── create_tables.py           # Script para criar tabelas
├── seed_brinquedos.py        # Script para popular brinquedos
├── test_brinquedos_api.py    # Testes automatizados
├── requirements.txt           # Dependências do projeto
├── alembic.ini               # Configuração do Alembic
├── render.yaml               # Configuração para deploy no Render
└── BRINQUEDOS_API_DOCS.md   # Documentação detalhada da API de Brinquedos
```

---

## 🎯 Módulos e Funcionalidades

### 1️⃣ Autenticação (`/auth`)
- ✅ Criar conta (POST `/auth/criar_conta`)
- ✅ Login (POST `/auth/login`)
- ✅ Alterar senha (PATCH `/auth/alterar_senha`)
- ✅ Atualizar usuário (PUT `/auth/atualizar_usuario/{id}`)
- ✅ Deletar usuário (DELETE `/auth/deletar_usuario/{id}`)

### 2️⃣ Clientes (`/cliente`)
- ✅ Listar clientes (GET `/cliente/`)
- ✅ Atualizar cliente (PUT `/cliente/atualizar_cliente/{id}`)
- ✅ Deletar cliente (DELETE `/cliente/deletar_cliente/{id}`)

### 3️⃣ Pets (`/pets`)
- ✅ Listar pets (GET `/pets/`)
- ✅ Cadastrar pet (POST `/pets/Cadastrar_pet`)
- ✅ Atualizar pet (PUT `/pets/atualizar_pet/{id}`)
- ✅ Deletar pet (DELETE `/pets/deletar_pet/{id}`)

### 4️⃣ Remédios (`/remedios`)
- ✅ Listar remédios (GET `/remedios/`)
- ✅ Cadastrar remédio (POST `/remedios/Cadastrar_remedio`)
- ✅ Atualizar remédio (PUT `/remedios/atualizar_remedio/{id}`)
- ✅ Deletar remédio (DELETE `/remedios/deletar_remedio/{id}`)

### 5️⃣ Brinquedos (`/brinquedos`) ✨ NOVO
- ✅ Listar com filtros (GET `/brinquedos/`)
- ✅ Buscar por ID (GET `/brinquedos/{id}`)
- ✅ Buscar por categoria (GET `/brinquedos/categoria/{categoria}`)
- ✅ Cadastrar brinquedo (POST `/brinquedos/cadastrar`)
- ✅ Atualizar brinquedo (PUT `/brinquedos/atualizar/{id}`)
- ✅ Atualizar estoque (PATCH `/brinquedos/estoque/{id}`)
- ✅ Deletar brinquedo (DELETE `/brinquedos/deletar/{id}`)
- ✅ Estatísticas (GET `/brinquedos/estatisticas/resumo`)

**Categorias de Brinquedos:**
- 🧸 Pelúcia
- ⚽ Bola
- 🧩 Interativo
- 🦴 Mordedor

### 6️⃣ Colaboradores (`/colaboradores`)
- ✅ Listar colaboradores (GET `/colaboradores/`)
- ✅ Cadastrar colaborador (POST `/colaboradores/Cadastrar_Colaborador`)
- ✅ Atualizar colaborador (PUT `/colaboradores/atualizar_colaborador/{id}`)
- ✅ Deletar colaborador (DELETE `/colaboradores/deletar_colaborador/{id}`)

### 7️⃣ Compras/Transações (`/compras`)
- ✅ Listar compras (GET `/compras/`)
- ✅ Criar compra (POST `/compras/criar`)
- ✅ Atualizar compra (PUT `/compras/atualizar_compra/{id}`)
- ✅ Deletar compra (DELETE `/compras/deletar_compra/{id}`)
- ✅ Controle automático de estoque

---

## 🧪 Testes

### Executar todos os testes da API de Brinquedos:

```bash
python test_brinquedos_api.py
```

### Testes incluem:
- ✅ CRUD completo
- ✅ Filtros e buscas
- ✅ Validações de dados
- ✅ Tratamento de erros
- ✅ Estatísticas

---

## 📖 Documentação

### Documentação Interativa (Swagger)
Acesse: http://localhost:8000/docs

### Documentação Detalhada
Veja o arquivo [`BRINQUEDOS_API_DOCS.md`](BRINQUEDOS_API_DOCS.md) para:
- 📝 Exemplos completos de uso
- 🔍 Detalhes de cada endpoint
- 💡 Boas práticas
- 🎨 Exemplos de integração com frontend

---

## 🛠️ Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validação de dados
- **Alembic** - Migrações de banco de dados
- **Passlib** - Criptografia de senhas (bcrypt)
- **Python-Jose** - Tokens JWT
- **Pandas** - Manipulação de dados
- **Uvicorn** - Servidor ASGI

---

## 🔒 Segurança

- ✅ Senhas criptografadas com bcrypt
- ✅ Validação de dados com Pydantic
- ✅ Proteção contra SQL Injection (SQLAlchemy)
- ✅ CORS configurado
- ✅ Variáveis de ambiente para secrets

---

## 🚢 Deploy

### Deploy no Render

O projeto está configurado para deploy automático no Render através do arquivo `render.yaml`.

1. Crie uma conta no [Render](https://render.com)
2. Conecte seu repositório GitHub
3. O deploy será automático!

### Variáveis de Ambiente para Produção

```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=sua_chave_super_secreta_aqui
```

---

## 📊 Banco de Dados

### Tabelas Criadas:

1. **usuarios** - Usuários do sistema
2. **clientes** - Clientes da loja
3. **pets** - Pets dos clientes
4. **remedios** - Medicamentos
5. **brinquedos** ✨ - Brinquedos para pets (NOVO!)
6. **colaboradores** - Funcionários
7. **transacoes** - Vendas e compras

### Migrações com Alembic

```bash
# Criar nova migração
alembic revision --autogenerate -m "descrição"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📝 Exemplos de Uso

### Cadastrar um Brinquedo

```python
import requests

brinquedo = {
    "nome": "Urso de Pelúcia",
    "categoria": "Pelúcia",
    "preco": 49.90,
    "estoque": 50,
    "imagem": "/imagens/urso.png",
    "descricao": "Brinquedo macio e seguro"
}

response = requests.post(
    "http://localhost:8000/brinquedos/cadastrar",
    json=brinquedo
)
print(response.json())
```

### Buscar Brinquedos por Categoria

```python
response = requests.get(
    "http://localhost:8000/brinquedos/categoria/Bola"
)
print(response.json())
```

### Atualizar Estoque

```python
response = requests.patch(
    "http://localhost:8000/brinquedos/estoque/1?quantidade=100"
)
print(response.json())
```

---

## 📞 Suporte

- 📧 Email: suporte@farmpet.com
- 🐛 Issues: [GitHub Issues](https://github.com/artzxvvs/api_farmpet/issues)
- 📖 Docs: http://localhost:8000/docs

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👥 Autores

- **artzxvvs** - [GitHub](https://github.com/artzxvvs)

---

## 🎉 Agradecimentos

- FastAPI pela excelente documentação
- Comunidade Python
- Todos os contribuidores

---

**Desenvolvido com ❤️ para FarmPet**

*Última atualização: Novembro 2025*
