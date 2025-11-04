from models import SessionLocal, Usuario, Cliente

session = SessionLocal()
try:
    u = session.query(Usuario).filter(Usuario.EMAIL=='teste2@example.com').first()
    if u:
        print('Usuario encontrado:', u.ID, u.EMAIL)
    else:
        print('Usuario nao encontrado')
    c = session.query(Cliente).filter(Cliente.CPF=='12345678900').first()
    if c:
        print('Cliente encontrado:', c.ID, c.NOME, c.ID_USUARIO)
    else:
        print('Cliente nao encontrado')
finally:
    session.close()
