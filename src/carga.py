import logging

import pandas as pd
from sqlalchemy import create_engine

from config import POSTGRES_URL

logger = logging.getLogger(__name__)

def load_postgresql(df):
    
    logger.info("Iniciando carga de dados no postgresSQL.")
    
    try:
        engine = create_engine(POSTGRES_URL)
        logger.info("conexão com o PostgreSQL criada")
        
        df.to_sql(
            name="indicadores_ibge",
            con=engine,
            if_exists="replace",
            index=False
        )
        logger.info("Dados carregados no PostgresSQL com sucesso")
        
        logger.info("Total de registros carregados: %s",
                    len(df)
                    )
    except Exception as erro:
        logger.error(
            "Erro durante a carga no PostgreSQL: %s",
            erro
        )
        raise
    
    finally:
        if "engine" in locals():
            engine.dispose()
            
            logger.info("Conexão com o postgreSQl encerrada")
            

if __name__ == "__main__":

    from src.extracao import extract
    from src.transformacao import transform
    from src.validacao import validate

    dados = extract()

    df = transform(dados)

    validate(df)

    load_postgresql(df)

    print("\nCarga no PostgreSQL realizada com sucesso!")