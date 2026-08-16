from sqlalchemy import create_engine, text

from config import POSTGRES_URL


engine = create_engine(POSTGRES_URL)


with engine.connect() as conexao:

    resultado = conexao.execute(
        text("SELECT version();")
    )

    print(resultado.fetchone())


engine.dispose()

print("Conexão realizada com sucesso!")