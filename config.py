import os

from dotenv import load_dotenv
from sqlalchemy import URL


load_dotenv()

url_ibge = (
    "https://apisidra.ibge.gov.br/"
    "values/t/4709/n6/2611606/p/2022/v/93"
)

nome_arquivo = "ibge_populacao"


# ---------------------------------------------------------
# PostgreSQL
# ---------------------------------------------------------

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")


POSTGRES_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=int(POSTGRES_PORT),
    database=POSTGRES_DB
)