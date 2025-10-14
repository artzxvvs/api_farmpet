from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # Carregar variáveis de ambiente do arquivo .env
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI() 
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# importar as rotas
from auth_routes import auth_router
from cliente_routes import cliente_router

# incluir as rotas ao app
app.include_router(auth_router)
app.include_router(cliente_router)