import json
import logging
from datetime import datetime
from pathlib import Path

import requests

from config import nome_arquivo
from config import url_ibge


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Extração
# ---------------------------------------------------------

def extract():
    """
    Consulta a API do IBGE e salva a resposta original
    na camada RAW.

    Retorna:
        dados: JSON retornado pela API.
    """

    logger.info("Iniciando extração dos dados do IBGE.")

    try:
        # -------------------------------------------------
        # Consulta à API
        # -------------------------------------------------

        resposta = requests.get(
            url_ibge,
            timeout=10
        )

        # Verifica se houve erro HTTP
        resposta.raise_for_status()

        logger.info(
            "Consulta ao IBGE realizada com sucesso. "
            "Status HTTP: %s",
            resposta.status_code
        )

        # Converte a resposta JSON para Python
        dados = resposta.json()

        # -------------------------------------------------
        # Localização da pasta RAW
        # -------------------------------------------------

        diretorio_projeto = (
            Path(__file__).resolve().parent.parent
        )

        diretorio_raw = diretorio_projeto / "raw"

        # Cria a pasta RAW caso ela não exista
        diretorio_raw.mkdir(
            parents=True,
            exist_ok=True
        )

        # -------------------------------------------------
        # Criação do nome do arquivo
        # -------------------------------------------------

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H%M"
        )

        nome_arquivo_raw = (
            f"{timestamp}_{nome_arquivo}.json"
        )

        caminho_arquivo = (
            diretorio_raw / nome_arquivo_raw
        )

        # -------------------------------------------------
        # Salvamento do JSON bruto
        # -------------------------------------------------

        with open(
            caminho_arquivo,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

        logger.info(
            "Dados RAW salvos em: %s",
            caminho_arquivo
        )

        return dados

    # -----------------------------------------------------
    # Tratamento de erros
    # -----------------------------------------------------

    except requests.exceptions.Timeout:

        logger.error(
            "Tempo limite excedido ao consultar o IBGE."
        )

        raise

    except requests.exceptions.HTTPError as erro:

        logger.error(
            "Erro HTTP ao consultar o IBGE: %s",
            erro
        )

        raise

    except requests.exceptions.RequestException as erro:

        logger.error(
            "Erro na requisição ao IBGE: %s",
            erro
        )

        raise

    except ValueError as erro:

        logger.error(
            "A resposta da API não contém um JSON válido: %s",
            erro
        )

        raise


# ---------------------------------------------------------
# Execução direta
# ---------------------------------------------------------

if __name__ == "__main__":
    extract()