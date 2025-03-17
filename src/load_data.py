import pandas as pd
from src.config import DATA_PATH


def load_data():
    return {
        "rais_anual": pd.read_csv(DATA_PATH / "rais_anual.csv", sep=";"),
        "caged_saldo_anual": pd.read_csv(
            DATA_PATH / "caged_saldo_movimentacao_anual.csv", encoding="latin1", sep=";"
        ),
        "caged_saldo_secao": pd.read_csv(
            DATA_PATH / "caged_saldo_secao.csv", sep=";", encoding="latin1"
        ),
        "caged_saldo_idade": pd.read_csv(
            DATA_PATH / "caged_saldo_idade.csv", sep=";", encoding="latin1"
        ),
        "caged_media_idade": pd.read_csv(
            DATA_PATH / "caged_media_idade.csv", sep=";", encoding="latin1"
        ),
        "caged_media_salario": pd.read_csv(
            DATA_PATH / "caged_media_salario.csv", sep=";", encoding="latin1"
        ),
        "pib_por_categoria": pd.read_csv(
            DATA_PATH / "pib_por_categoria.csv", sep=";", encoding="latin1"
        ),
        "pib_participacao_sp": pd.read_csv(
            DATA_PATH / "pib_participacao_sp.csv", sep=";", encoding="latin1"
        ),
        "pib_per_capita": pd.read_csv(
            DATA_PATH / "pib_per_capita.csv", sep=";", encoding="latin1"
        ),
    }
