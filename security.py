from passlib.context import CryptContext

# Contexto compartilhado para hashing de senhas
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
