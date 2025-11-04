import traceback
from models import SessionLocal, Usuario, Cliente
from security import bcrypt_context

def run_test():
    session = SessionLocal()
    try:
        nome = 'ScriptTeste'
        email = 'script_teste@example.com'
        senha = '123456'
        rua = 'Rua Script'
        numero = '1'
        bairro = 'Centro'
        complemento = 'A'
        telefone = '11900000000'
        cpf = '99988877766'

        senha_criptografada = bcrypt_context.hash(senha)
        novo_usuario = Usuario(nome, email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
        print('Usuario criado id=', novo_usuario.ID)

        try:
            novo_cliente = Cliente(
                NOME=nome,
                RUA=rua,
                NUMERO=numero,
                BAIRRO=bairro,
                COMPLEMENTO=complemento,
                TELEFONE=telefone,
                ID_USUARIO=novo_usuario.ID,
                CPF=cpf,
            )
            session.add(novo_cliente)
            session.commit()
            session.refresh(novo_cliente)
            print('Cliente criado id=', novo_cliente.ID)
        except Exception as e:
            session.rollback()
            print('Erro ao criar cliente:')
            traceback.print_exc()
    except Exception:
        session.rollback()
        print('Erro ao criar usuario:')
        traceback.print_exc()
    finally:
        session.close()

if __name__ == '__main__':
    run_test()
