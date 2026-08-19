import logging

from src.extracao import extract
from src.transformacao import transform
from src.validacao import validate
from src.carga import load_postgresql
from src.mongo import load_mongodb


# ---------------------------------------------------------
# Configuração do logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Pipeline
# ---------------------------------------------------------

def run_pipeline():

    logger.info("=" * 60)
    logger.info("INICIANDO PIPELINE DE INDICADORES DO IBGE")
    logger.info("=" * 60)

    try:

        # -------------------------------------------------
        # 1. EXTRAÇÃO
        # -------------------------------------------------

        logger.info("ETAPA 1/5 - EXTRAÇÃO")

        dados = extract()

        logger.info(
            "Extração concluída com sucesso."
        )

        # -------------------------------------------------
        # 2. TRANSFORMAÇÃO
        # -------------------------------------------------

        logger.info("ETAPA 2/5 - TRANSFORMAÇÃO")

        df = transform(dados)

        logger.info(
            "Transformação concluída com sucesso."
        )

        # -------------------------------------------------
        # 3. VALIDAÇÃO
        # -------------------------------------------------

        logger.info("ETAPA 3/5 - VALIDAÇÃO")

        validate(df)

        logger.info(
            "Validação concluída com sucesso."
        )

        # -------------------------------------------------
        # 4. POSTGRESQL
        # -------------------------------------------------

        logger.info("ETAPA 4/5 - POSTGRESQL")

        load_postgresql(df)

        logger.info(
            "Carga no PostgreSQL concluída com sucesso."
        )

        # -------------------------------------------------
        # 5. MONGODB
        # -------------------------------------------------

        logger.info("ETAPA 5/5 - MONGODB")

        load_mongodb(df)

        logger.info(
            "Carga no MongoDB concluída com sucesso."
        )

        # -------------------------------------------------
        # FINALIZAÇÃO
        # -------------------------------------------------

        logger.info("=" * 60)
        logger.info("PIPELINE EXECUTADO COM SUCESSO!")
        logger.info("=" * 60)

    except Exception as erro:

        logger.error("=" * 60)
        logger.error("PIPELINE INTERROMPIDO!")
        logger.error("Motivo: %s", erro)
        logger.error("=" * 60)

        raise


# ---------------------------------------------------------
# Execução
# ---------------------------------------------------------

if __name__ == "__main__":
    run_pipeline()