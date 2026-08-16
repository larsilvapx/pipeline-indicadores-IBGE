import logging

import pandas as pd

# Logging

logger = logging.getLogger(__name__)

## Transformação:

def transform(dados):
    
    logger.info("Iniciando a transformação dos dados.")
    
    df = pd.DataFrame(dados)
    
    logger.info(
        "Dataframe criado em %s linhas e %s colunas",
        df.shape[0],
        df.shape[1]
    )
    df = df.rename(
         columns={
             "D1N": "localidade",
            "D2N": "periodo",
            "D3N": "indicador",
            "V": "valor"
         }
     )
    logger.info("Colunas renomeadas com sucesso!")
    
    colunas = [
        "localidade",
        "periodo",
        "indicador",
        "valor"
    ]
    df = df[colunas]
    
    df["valor"] = pd.to_numeric(
        df["valor"],
        errors="coerce"
    )
    logger.info(
        "Transformação concluída com sucesso"
    )
    return df

if __name__ == "__main__":
    from src.extracao import extract
    
    dados = extract
    
    df = transform(dados)
    
    print("\n Dataframe transformado")
    print(df)
    
    print("\n tipos de colunas: ")
    print(df.dtypes)