import logging

import pandas as pd

logger = logging.getLogger(__name__)

colunas_obrigatorias = [
    "localidade",
    "periodo",
    "indicador",
    "valor"
]

def validate(df):
    if df.empty:
        logger.error("Validação falhou, Dataframe vazio")
        
        raise ValueError( "O dataFrame esá vazio")
    
    logger.info(
        "Validação 1/4 Datframe possui dados. "
        "Total de registros %s",
        len(df)
    )
    
    colunas_faltantes = [
        coluna
        for coluna in colunas_obrigatorias
        if coluna not in df.columns            
    ]
    
    if colunas_faltantes:
        logger.error(
            "Validação falhor: colunas obrigatorias"
            "ausentes %",
            colunas_faltantes
        )
        
        raise ValueError(
            f"Colunas obrigatorias ausentes:"
            f"{colunas_faltantes}"
        )
        
    logger.info(
        "Validação 2/4: todas colunas orbigatorias "
        "estão presentes"
    )
    
    nulos = df[colunas_obrigatorias].isnull().sum()
    total_nulos = nulos.sum()
     
    if total_nulos > 0:
         logger.error(
             "Validação falhor: existem %s valores nulos.",
             total_nulos
         )
         
         logger.error(
             "Quantidade de nulos por coluna: \n%s",
             nulos[nulos>0]             
         )
         
         raise ValueError(
             "existem valores nulos nos dados."
         )
         
    logger.info(
        "Validação 3/4: nenhum valor encontrado."
    )
    
    if not pd.api.types.is_numeric_dtype(df["valor"]):
        
        logger.error(
            "Validação falhou: coluna 'valor"
            "não é numerica"
        )
        raise ValueError ("A coluna valor precisa ser numerica")
    logger.info(
        "Validação 4/4: coluna 'valor' é numerica."
    )
    
    logger.info("Validação realizada com sucesso!")
    
    return True

if __name__ == "__main__":
    from src.extracao import extract
    from src.transformacao import transform

    dados = extract()

    df = transform(dados)

    validate(df)

    print("\nValidação aprovada!")
    
