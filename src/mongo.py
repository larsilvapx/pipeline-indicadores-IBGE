import logging

import pandas as pd
from pymongo import MongoClient

from config import MONGO_URL


logger = logging.getLogger(__name__)


def criar_resumo(df):
   

    logger.info("Iniciando criação da coleção derivada.")

    resumo = (
        df.groupby(
            ["localidade", "indicador"],
            as_index=False
        )
        .agg(
            quantidade_registros=("valor", "count"),
            valor_minimo=("valor", "min"),
            valor_maximo=("valor", "max"),
            valor_medio=("valor", "mean")
        )
    )

    logger.info(
        "Coleção derivada criada com %s registros.",
        len(resumo)
    )

    return resumo


def load_mongodb(df):

    logger.info("Iniciando carga dos dados no MongoDB Atlas.")

    cliente = None

    try:

        

        cliente = MongoClient(
            MONGO_URL,
            serverSelectionTimeoutMS=5000
        )

        # Teste da conexão
        cliente.admin.command("ping")

        logger.info(
            "Conexão com MongoDB Atlas realizada com sucesso."
        )

        

        resumo = criar_resumo(df)

        documentos = resumo.to_dict(
            orient="records"
        )

        logger.info(
            "Total de documentos derivados: %s",
            len(documentos)
        )

        

        banco = cliente["indicadores_ibge"]

        colecao = banco["resumo_indicadores"]

        logger.info(
            "Collection 'resumo_indicadores' selecionada."
        )

        

        colecao.delete_many({})

        logger.info(
            "Collection anterior limpa."
        )

        

        if documentos:

            resultado = colecao.insert_many(
                documentos
            )

            logger.info(
                "Dados carregados no MongoDB com sucesso."
            )

            logger.info(
                "Total de documentos inseridos: %s",
                len(resultado.inserted_ids)
            )

        else:

            logger.warning(
                "Nenhum documento disponível para carga."
            )

    except Exception as erro:

        logger.error(
            "Erro durante a carga no MongoDB: %s",
            erro
        )

        raise

    finally:

        if cliente:

            cliente.close()

            logger.info(
                "Conexão com MongoDB encerrada."
            )


if __name__ == "__main__":

    from src.extracao import extract
    from src.transformacao import transform
    from src.validacao import validate

    dados = extract()

    df = transform(dados)

    validate(df)

    load_mongodb(df)

    print(
        "\nCarga derivada no MongoDB realizada com sucesso!"
    )