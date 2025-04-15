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
            DATA_PATH / "pib_participacao_sp_munic_selecionados.csv", sep=";", encoding="latin1"
        ),
        "pib_per_capita": pd.read_csv(
            DATA_PATH / "pib_per_capita_munic_selecionados.csv", sep=";", encoding="latin1"
        ),
        "pbf_munic_selecionados": pd.read_csv(
            DATA_PATH / "pbf_munic_selecionados.csv", sep=";", encoding="latin1"
        ),
        "arrecadacao": pd.read_csv(
            DATA_PATH / "tb_sigt_arrecadacao.csv", sep=";", encoding="latin1"
        ),
        "atraso_tributos": pd.read_csv(
            DATA_PATH / "tb_sigt_atraso_tributo.csv", sep=";", encoding="latin1"
        ),
        "previsao_arrecadacao": pd.read_csv(
            DATA_PATH / "tb_sigt_previsao_arrecadacao.csv", sep=";", encoding="latin1"
        ),
        "abertura_encerramento_empresas_cleaned": pd.read_csv(
            DATA_PATH / "tb_sigt_abertura_encerramento_empresas_cleaned.csv", sep=";"
        ),
    }
