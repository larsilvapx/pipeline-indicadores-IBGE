import logging

from pymongo import MongoClient

from config import MONGO_URL


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def testar_mongodb():

    logger.info("Iniciando teste de conexão com MongoDB Atlas.")

    cliente = None

    try:
        cliente = MongoClient(
            MONGO_URL,
            serverSelectionTimeoutMS=5000
        )

        # Testa efetivamente a conexão
        cliente.admin.command("ping")

        logger.info("Conexão com MongoDB Atlas realizada com sucesso!")

        print("\nMongoDB conectado com sucesso!")

    except Exception as erro:

        logger.error(
            "Erro ao conectar ao MongoDB: %s",
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
    testar_mongodb()