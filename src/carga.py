import logging

import pandas as pd
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import insert

from config import POSTGRES_URL




logger = logging.getLogger(__name__)



def load_postgresql(df):

    logger.info(
        "Iniciando carga de dados no PostgreSQL."
    )

    engine = None

    try:

        

        engine = create_engine(POSTGRES_URL)

        logger.info(
            "Conexão com o PostgreSQL criada."
        )


        metadata = MetaData()

        tabela = Table(
            "indicadores_ibge",
            metadata,

            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True
            ),

            Column(
                "localidade",
                String,
                nullable=False
            ),

            Column(
                "periodo",
                String,
                nullable=False
            ),

            Column(
                "indicador",
                String,
                nullable=False
            ),

            Column(
                "valor",
                Float,
                nullable=False
            ),

            UniqueConstraint(
                "localidade",
                "periodo",
                "indicador",
                name="uq_indicador_ibge"
            )
        )

        

        metadata.create_all(engine)

        logger.info(
            "Tabela 'indicadores_ibge' verificada/criada."
        )

        

        registros = df.to_dict(
            orient="records"
        )

        logger.info(
            "Total de registros recebidos para carga: %s",
            len(registros)
        )


        if registros:

            comando = insert(tabela).values(
                registros
            )

            comando = comando.on_conflict_do_nothing(
                constraint="uq_indicador_ibge"
            )

            with engine.begin() as conexao:

                resultado = conexao.execute(
                    comando
                )

            logger.info(
                "Carga executada com sucesso."
            )

            logger.info(
                "Novos registros inseridos: %s",
                resultado.rowcount
            )

        else:

            logger.warning(
                "Nenhum registro disponível para carga."
            )

    except Exception as erro:

        logger.error(
            "Erro durante a carga no PostgreSQL: %s",
            erro
        )

        raise

    finally:

        if engine is not None:

            engine.dispose()

            logger.info(
                "Conexão com o PostgreSQL encerrada."
            )




if __name__ == "__main__":

    from src.extracao import extract
    from src.transformacao import transform
    from src.validacao import validate

    dados = extract()

    df = transform(dados)

    validate(df)

    load_postgresql(df)

    logger.info(
        "Pipeline de carga finalizado com sucesso."
    )