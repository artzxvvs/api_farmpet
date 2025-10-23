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
from remedio_routes import remedios_router
from pet_routes import pet_router
from colaborador_routes import colaborador_router
from compra_routes import compra_router
# incluir as rotas ao app
app.include_router(colaborador_router)
app.include_router(auth_router)
app.include_router(cliente_router)
app.include_router(remedios_router)
app.include_router(pet_router)
app.include_router(compra_router)