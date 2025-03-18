from dash import html
import dash_bootstrap_components as dbc
from babel.numbers import format_currency, format_percent, format_compact_currency

def get_options_dropdown(all_data, table, column):
    sorted_values = sorted(all_data[table][column].dropna().unique())
    return [{"label": x, "value": x} for x in sorted_values]

def calcular_pib_atual(pib_por_categoria):
    ano_max = pib_por_categoria["ano"].max()
    pib_corrente_int = (
        pib_por_categoria.loc[
            (pib_por_categoria["ano"] == ano_max)
            & (pib_por_categoria["variavel_dash"] == "Total")
        ]["pib_corrente"]
        .values[0]
        .round()
        .astype(int)
    )
    pib_corrente = format_compact_currency(pib_corrente_int, 'BRL', locale='pt_BR', fraction_digits=2)
    return pib_corrente


def calcular_variacao_pib(pib_por_categoria):
    pib_ano = (
        pib_por_categoria.loc[
            (pib_por_categoria["ano"] == pib_por_categoria["ano"].max())
            & (pib_por_categoria["variavel_dash"] == "Total")
        ]["pib_deflacionado"]
        .values[0]
        .round()
        .astype(int)
    )

    pib_ano_anterior = (
        pib_por_categoria.loc[
            (pib_por_categoria["ano"] == pib_por_categoria["ano"].max() - 1)
            & (pib_por_categoria["variavel_dash"] == "Total")
        ]["pib_deflacionado"]
        .values[0]
        .round()
        .astype(int)
    )

    variacao_pib = ((pib_ano - pib_ano_anterior) / pib_ano_anterior)
    variacao_pib = format_percent(variacao_pib, format='#,##0.0%', locale='pt_BR')

    return variacao_pib