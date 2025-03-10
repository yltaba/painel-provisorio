import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from pathlib import Path
import plotly.express as px

TEMPLATE = "plotly_white"

pib_por_categoria = pd.read_csv(
    "data/pib_por_categoria.csv", sep=";", encoding="latin1"
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

dash.register_page(__name__)
layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Desenvolvimento Econômico"),
                dcc.Graph(id="fig-pib-categorias", figure=fig_pib_categorias),
            ]
        )
    ]
)
