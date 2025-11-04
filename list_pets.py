from models import SessionLocal, Pet

session = SessionLocal()
try:
    pets = session.query(Pet).all()
    for p in pets:
        print('Pet', p.ID, getattr(p, 'NOME', None), getattr(p, 'ID_CLIENTE', None))
finally:
    session.close()
