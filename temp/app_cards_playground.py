import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pathlib import Path
import plotly.express as px
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

data_path = Path().resolve() / "data"
TEMPLATE = "plotly_white"

# Carregar os dados
pib_por_categoria = pd.read_csv(
    data_path / "pib_por_categoria.csv", sep=";", encoding="latin1"
)


# Dados Card

# pib total
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
pib_corrente = locale.format_string('%.0f', pib_corrente_int, grouping=True)

# variação % do PIB
pib_ano = pib_por_categoria.loc[
    (pib_por_categoria["ano"] == pib_por_categoria["ano"].max())
    & (pib_por_categoria["variavel_dash"] == "Total")
]['pib_deflacionado'].values[0].round().astype(int)

pib_ano_anterior = pib_por_categoria.loc[
    (pib_por_categoria["ano"] == pib_por_categoria["ano"].max() - 1)
    & (pib_por_categoria["variavel_dash"] == "Total")
]['pib_deflacionado'].values[0].round().astype(int)

variacao_pib = ((pib_ano - pib_ano_anterior) / pib_ano_anterior) * 100
variacao_pib = locale.format_string("%.1f%%", variacao_pib, grouping=True)

# Imagem do cabeçalho
imagem_cabecalho = html.Img(
    src="https://osasco.sp.gov.br/wp-content/uploads/2024/12/logo-pmo-2025-2028-horizontal.png",
    style={
        "width": "50%",
        "height": "50%",
        "display": "block",
        "margin": "auto",
        "margin-top": "30px",
    },
)

# Layout
external_stylesheets = [dbc.themes.MORPH]
app = dash.Dash(
    external_stylesheets=external_stylesheets, suppress_callback_exceptions=True
)

# DADOS PIB

titulo_grafico = html.H1("Evolução do PIB de Osasco")
card_pib_corrente = dbc.Card(
    dbc.CardBody(
        [
            html.H5(f"PIB {ano_max}", className="card-title"),
            html.Div(
                [
                    html.Span("R$ ", className="currency-symbol"),
                    html.Span(pib_corrente, className="card-value")
                ],
                className="card-value-container"
            ),
        ]
    ),
    className="custom-card"
)
card_variacao_pib = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Variação % 2020-2021", className="card-title"),
            html.Div(
                [
                    html.Span(variacao_pib, className="card-value")
                ],
                className="card-value-container"
            ),
        ]
    ),
    className="custom-card"
)

fig_pib_categorias = px.line(
    pib_por_categoria,
    x="ano",
    y="pib_deflacionado",
    color="variavel_dash",
    labels={
        "ano": "Ano",
        "pib_deflacionado": "PIB (deflacionado)",
        "variavel_dash": "Categoria",
    },
    markers=True,
    template=TEMPLATE,
)
fig_pib_categorias.update_xaxes(tickmode="linear", tickangle=45)


cards_column = dbc.Col(
    [
        card_pib_corrente,
        html.Div(style={"height": "20px"}),  # Spacer between cards
        card_variacao_pib
    ],
    width=3,
    className="cards-container"
)

main_row = dbc.Row(
    [
        cards_column,  # Cards stacked vertically on the left
        dbc.Col(
            dcc.Graph(
                id='pib-graph',
                figure=fig_pib_categorias  # Your plot figure
            ),
            width=9
        )
    ],
    className="main-content-row"
)

app.layout = dbc.Container(
    [
        imagem_cabecalho,
        html.Br(),
        titulo_grafico,
        main_row,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
