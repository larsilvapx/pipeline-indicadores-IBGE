===== ## Pipeline de Indicadores IBGE ## =====


Pipeline de Engenharia de Dados desenvolvido em Python para realizar a
extração, transformação, validação e carga de indicadores do IBGE,
utilizando uma API pública como fonte e persistindo os dados em
PostgreSQL e MongoDB Atlas.

O projeto foi estruturado de forma modular, com separação de
responsabilidades entre as etapas do pipeline, geração de arquivos RAW
com timestamp, logging, validação dos dados e armazenamento em bancos
com diferentes finalidades.

 # Visão geral

O objetivo deste projeto é demonstrar, de forma prática, um fluxo
completo de Engenharia de Dados:

API IBGE
   ↓
Extração
   ↓
Dados RAW
   ↓
Transformação
   ↓
Validação
   ↓
┌───────────────┬────────────────────┐
│ PostgreSQL    │ MongoDB Atlas      │
│ dados tratados│ coleção derivada   │
└───────────────┴────────────────────┘

A fonte utilizada é a API de Agregados do IBGE/SIDRA, inicialmente
com uma consulta relacionada à população residente do município de
Recife (PE), no ano de 2022.

 # Objetivos do projeto

Consumir dados de uma API pública do IBGE.

Registrar a resposta original da API em arquivos JSON.

Manter os dados RAW separados dos dados tratados.

Transformar os dados recebidos em um DataFrame do Pandas.

Remover estruturas auxiliares da resposta SIDRA, como a linha de
cabeçalho.

Padronizar os nomes das colunas.

Validar a qualidade dos dados antes da carga.

Persistir os dados tratados no PostgreSQL.

Criar uma visão/coleção derivada no MongoDB Atlas.

Utilizar logging para acompanhar a execução.

Centralizar configurações de conexão.

Criar um orquestrador (main.py) para executar o pipeline completo.

Manter uma estrutura de projeto organizada e preparada para
evolução.

 # Arquitetura do projeto

Fluxograma

O fluxo arquitetural do projeto é representado abaixo:



Leitura do fluxo

API Agregados IBGE
Fonte dos dados utilizados pelo pipeline.

EXTRACT
A aplicação Python utiliza requests para realizar a requisição
HTTP e logging para registrar o processo.

RAW/JSON
A resposta original da API é armazenada em arquivos JSON com
timestamp. Isso permite preservar a informação recebida antes das
transformações.

TRANSFORM
Os dados são convertidos para um DataFrame utilizando Pandas,
tratados e preparados para as etapas seguintes.

Validação
O DataFrame é verificado antes da persistência.

PostgreSQL
Recebe os dados tratados em formato tabular.

MongoDB Atlas
Recebe uma coleção derivada, criada a partir dos dados tratados. A
finalidade não é simplesmente duplicar a tabela do PostgreSQL.

 # Fluxo completo do pipeline

O pipeline é executado seguindo esta sequência:

                ┌─────────────────────┐
                │     API IBGE        │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     EXTRAÇÃO        │
                │    extracao.py      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     RAW / JSON      │
                │ arquivos timestamp  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    TRANSFORMAÇÃO    │
                │  transformacao.py   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │      VALIDAÇÃO      │
                │    validacao.py     │
                └──────────┬──────────┘
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
          ┌────────────────┐ ┌──────────────────┐
          │  PostgreSQL    │ │  MongoDB Atlas   │
          │ dados tratados │ │ coleção derivada │
          └────────────────┘ └──────────────────┘

 # Estrutura do projeto

pipeline-indicadores-IBGE/
│
├── raw/
│   └── YYYY-MM-DD_HHMM_ibge_populacao.json
│
├── docs/
│   └── fluxograma.png
│
├── evidencias/
│   └── evidências da execução do projeto
│
├── src/
│   ├── __init__.py
│   ├── extracao.py
│   ├── transformacao.py
│   ├── validacao.py
│   ├── carga.py
│   ├── mongo.py
│   └── main.py
│
├── .gitignore
├── config.py
├── README.md
└── requirements.txt

# Responsabilidade de cada módulo

Arquivo              Responsabilidade

extracao.py        Consulta a API do IBGE e salva o JSON RAW
transformacao.py   Converte e trata os dados utilizando Pandas
validacao.py       Verifica se os dados estão aptos para carga
carga.py           Realiza a carga dos dados tratados no PostgreSQL
mongo.py           Cria e carrega a coleção derivada no MongoDB
main.py            Orquestra todas as etapas do pipeline
config.py          Centraliza configurações e strings de conexão
raw/               Armazena as respostas originais da API
evidencias/        Reúne evidências das execuções
docs/              Documentação visual do projeto

 # Tecnologias utilizadas

Python

Linguagem principal utilizada para implementar o pipeline.

Requests

Utilizada para realizar as requisições HTTP à API do IBGE.

Pandas

Utilizado para transformar, organizar e validar os dados em formato
tabular.

Logging

Utilizado para registrar o andamento do pipeline, sucessos e erros.

PostgreSQL

Banco relacional utilizado para armazenar os dados tratados.

SQLAlchemy

Utilizado como camada de conexão entre Python/Pandas e PostgreSQL.

Psycopg2

Driver utilizado para comunicação com PostgreSQL.

MongoDB Atlas

Banco NoSQL utilizado para armazenar uma coleção derivada dos dados.

PyMongo

Driver Python utilizado para conexão e operações com MongoDB.

 Fonte dos dados

Os dados são obtidos através da API de Agregados do IBGE/SIDRA.

A consulta utilizada na primeira versão do projeto está relacionada ao
indicador:

População residente

Para o município:

Recife (PE)

No período:

2022

# Exemplo do dado tratado:

localidade: Recife (PE)
periodo: 2022
indicador: População residente
valor: 1488920

1️ Extração

A primeira etapa do pipeline está implementada em:

src/extracao.py

O processo realiza:

API IBGE
   ↓
requests.get()
   ↓
verificação do status HTTP
   ↓
resposta JSON
   ↓
arquivo RAW

A requisição utiliza timeout e tratamento de exceções.

Exemplo conceitual:

resposta = requests.get(
    url_ibge,
    timeout=10
)

resposta.raise_for_status()

dados = resposta.json()

 Armazenamento RAW

Uma característica importante do projeto é a preservação dos dados
brutos.

Os arquivos são armazenados com timestamp:

raw/
└── 2026-08-16_2002_ibge_populacao.json

O padrão utilizado é:

YYYY-MM-DD_HHMM_nome_do_arquivo.json

Isso permite identificar quando cada coleta foi realizada e preservar o
estado original da fonte.

Por que manter RAW?

Porque em Engenharia de Dados é importante separar:

Dado original
     ↓
Dado tratado
     ↓
Dado validado
     ↓
Dado persistido

Caso exista algum problema durante a transformação, o dado original
continua disponível para auditoria e reprocessamento.

2️ Transformação

A transformação está implementada em:

src/transformacao.py

Nesta etapa a resposta da API é convertida em um DataFrame.

Um problema encontrado durante o desenvolvimento foi a presença da linha
de cabeçalho da estrutura SIDRA como uma linha do próprio DataFrame:

    localidade periodo       indicador   valor
0   Município  Ano             Variável    NaN
1   Recife     2022            População  1488920

Essa linha foi identificada e removida durante o tratamento.

Resultado final:

    localidade   periodo             indicador               valor
0   Recife (PE)  2022                População residente    1488920

3️ Validação

A validação está implementada em:

src/validacao.py

Foram definidos campos obrigatórios:

colunas_obrigatorias = [
    "localidade",
    "periodo",
    "indicador",
    "valor"
]

O processo realiza quatro verificações principais.

1. DataFrame possui dados

DataFrame vazio
       ↓
   erro

Caso contrário:

DataFrame possui dados
       ↓
   continua

2. Colunas obrigatórias

O pipeline verifica se todas as colunas necessárias existem.

3. Valores nulos

São verificados valores nulos nas colunas obrigatórias.

Durante o desenvolvimento foi encontrado um problema:

valor
NaN

A causa foi a linha de cabeçalho SIDRA que havia sido interpretada como
registro.

Após a correção da transformação:

Valores nulos:
Empty DataFrame

4. Tipo numérico

A coluna valor precisa ser numérica.

pd.api.types.is_numeric_dtype(
    df["valor"]
)

Somente depois que todas as validações são aprovadas o dado segue para
as bases.

4️ PostgreSQL

A carga no PostgreSQL está implementada em:

src/carga.py

O PostgreSQL funciona como o destino relacional dos dados tratados.

A tabela utilizada é:

indicadores_ibge

Com os campos principais:

localidade
periodo
indicador
valor

Exemplo:

localidade    periodo   indicador                 valor

Recife (PE)   2022      População residente     1488920

A conexão é realizada através do SQLAlchemy.

5️ MongoDB Atlas

O MongoDB foi utilizado como segundo destino, porém com uma finalidade
diferente.

A proposta não é simplesmente copiar a tabela do PostgreSQL.

O mongo.py cria uma coleção derivada.

A coleção utilizada é:

resumo_indicadores

Os dados são agrupados por:

localidade
indicador

E são calculadas informações como:

quantidade_registros
valor_minimo
valor_maximo
valor_medio

Exemplo:

{
    "localidade": "Recife (PE)",
    "indicador": "População residente",
    "quantidade_registros": 1,
    "valor_minimo": 1488920,
    "valor_maximo": 1488920,
    "valor_medio": 1488920.0
}

Dessa forma:

PostgreSQL
→ dados tratados

MongoDB
→ visão derivada/resumida

Essa separação evita que o MongoDB seja apenas uma cópia da tabela
relacional.

# Configuração

As informações de conexão ficam centralizadas no:

config.py

Exemplos de configurações utilizadas:

URL_IBGE = "..."

POSTGRES_URL = "..."

MONGO_URL = "..."

⚠️ Nunca publique senhas, tokens ou strings de conexão contendo
credenciais em um repositório público.

Recomenda-se utilizar variáveis de ambiente ou um arquivo .env
ignorado pelo Git.

# Como executar o projeto

1. Clonar o repositório

git clone <URL_DO_REPOSITORIO>

Depois:

cd pipeline-indicadores-IBGE

2. Criar ambiente virtual

No Windows:

python -m venv .venv

Ativar:

.venv\Scripts\activate

3. Instalar dependências

pip install -r requirements.txt

4. Configurar as conexões

Configure no config.py ou através das variáveis de ambiente utilizadas
pelo projeto:

IBGE
PostgreSQL
MongoDB Atlas

Não publique credenciais no GitHub.

5. Executar o pipeline

A execução recomendada é:

python -m src.main

O main.py executa as etapas na ordem:

1. Extração
2. Transformação
3. Validação
4. PostgreSQL
5. MongoDB

# Logging

O projeto utiliza o módulo nativo:

import logging

Os logs permitem acompanhar o pipeline sem precisar adicionar vários
print() pelo código.

Exemplo:

INFO - Iniciando extração dos dados do IBGE.
INFO - Consulta ao IBGE realizada com sucesso. Status HTTP: 200
INFO - Dados RAW salvos em: .../raw/2026-08-16_2002_ibge_populacao.json
INFO - Iniciando a transformação dos dados.
INFO - Transformação concluída com sucesso
INFO - Validação realizada com sucesso!
INFO - Dados carregados no PostgreSQL com sucesso
INFO - Dados carregados no MongoDB com sucesso
INFO - PIPELINE EXECUTADO COM SUCESSO!

Em caso de falha, o pipeline registra o erro e interrompe a execução.

# Validações realizadas durante o desenvolvimento

Durante a construção do projeto foram identificados e corrigidos
problemas reais, incluindo:

Importação de configuração

Foi encontrado:

ModuleNotFoundError: No module named 'config'

A solução foi executar os módulos a partir da raiz utilizando:

python -m src.nome_do_modulo

Estrutura da resposta SIDRA

A API retornava uma linha de cabeçalho que estava sendo interpretada
pelo Pandas como dado.

Isso provocava:

valor = NaN

A linha foi removida durante a transformação.

Validação de dados

O pipeline inicialmente falhava porque existia um valor nulo:

Validação falhou: existem 1 valores nulos.

Após a correção:

Validação 1/4
Validação 2/4
Validação 3/4
Validação 4/4

Validação realizada com sucesso!

Conexão PostgreSQL

Também foi identificado um problema de codificação/credenciais na string
de conexão.

Após a correção, a conexão passou a funcionar e os dados foram
carregados.

MongoDB Atlas

Durante a configuração inicial foi encontrado:

bad auth : authentication failed

O problema estava relacionado à autenticação do usuário do MongoDB
Atlas.

Após a correção das credenciais, a conexão foi validada com sucesso.

# Resultado atual

A primeira versão funcional do pipeline consegue:

                 IBGE
                  │
                  ▼
              Extração
                  │
                  ▼
             JSON RAW
                  │
                  ▼
           Transformação
                  │
                  ▼
             Validação
              │       │
              │       │
              ▼       ▼
         PostgreSQL  MongoDB
         tratado     derivado

Foi validado um registro de população:

Localidade: Recife (PE)
Período: 2022
Indicador: População residente
Valor: 1.488.920

No MongoDB Atlas, a carga foi confirmada com sucesso e o documento
derivado foi armazenado na coleção correspondente.

# Próximas evoluções

A arquitetura foi construída de forma modular para permitir a expansão
do projeto.

Próximas possibilidades:

Adicionar novos indicadores do IBGE.

Adicionar mais municípios.

Trabalhar com séries históricas.

Criar novas consultas à API SIDRA.

Melhorar a estratégia de carga incremental.

Criar testes automatizados.

Adicionar validações mais avançadas.

Criar logs persistidos em arquivo.

Automatizar a execução do pipeline.

Criar dashboards utilizando os dados armazenados.

Evoluir o projeto para uma arquitetura de produção.

# Conceitos de Engenharia de Dados aplicados

Este projeto permite demonstrar conceitos importantes de Engenharia de
Dados:

ETL

Extract
   ↓
Transform
   ↓
Load

Data Lake / RAW

Preservação dos dados brutos antes da transformação.

Data Quality

Validação de:

existência de dados;

colunas obrigatórias;

valores nulos;

tipos de dados.

Data Persistence

Armazenamento dos dados em bancos distintos.

SQL

Utilização do PostgreSQL como banco relacional.

NoSQL

Utilização do MongoDB como banco orientado a documentos.

Logging

Observabilidade básica do pipeline.

Modularização

Cada etapa possui uma responsabilidade específica.

Orquestração

O main.py coordena a execução das etapas.

# Autor

Luciano Rodrigues

Projeto desenvolvido como exercício prático de Engenharia de Dados, com
foco em:

Python
APIs
Pandas
ETL
PostgreSQL
MongoDB
Logging
Qualidade de dados
Arquitetura de pipelines

# Licença

Este projeto foi desenvolvido para fins educacionais e de portfólio.