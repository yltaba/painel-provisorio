import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from pathlib import Path
import plotly.express as px

TEMPLATE = "plotly_white"

# Carregar os dados
rais_anual = pd.read_csv("data/rais_anual.csv", sep=";")

#
opcoes_cnae_rais = [
    {"label": x, "value": x}
    for x in sorted(rais_anual["descricao_secao_cnae"].dropna().unique())
]

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


# Layout da aplicação Dash
dash.register_page(__name__)

layout = dbc.Container(
    [
        html.Br(),
        html.H1("Desenvolvimento Econômico"),
        html.Br(),
        # Dados RAIS
        html.Div(
            [
                html.H4("Estoque de postos de trabalho por ano"),
                # Dropdown filtro fig-saldo-anual
                html.Label(
                    "Selecione uma Seção da CNAE:", style={"fontWeight": "light"}
                ),
                dcc.Dropdown(
                    id="filtro-cnae-rais-saldo",
                    options=[{"label": "Todos", "value": "Todos"}] + opcoes_cnae_rais,
                    value="Todos",
                    clearable=False,
                    className="mb-3",
                ),
                # Gráfico
                dcc.Graph(id="fig-rais-anual"),
            ]
        ),
    ]
)


@callback(Output("fig-rais-anual", "figure"), Input("filtro-cnae-rais-saldo", "value"))
def atualizar_grafico_rais_anual(filtro_cnae):
    if filtro_cnae == "Todos":
        df_filtrado = rais_anual
    else:
        df_filtrado = rais_anual[rais_anual["descricao_secao_cnae"] == filtro_cnae]

    rais_anual_grp = df_filtrado.groupby("ano", as_index=False).agg(
        {"quantidade_vinculos_ativos": "sum"}
    )

    fig = px.area(
        rais_anual_grp,
        x="ano",
        y="quantidade_vinculos_ativos",
        labels={
            "ano": "Ano",
            "quantidade_vinculos_ativos": "Quantidade de vínculos empregatícios ativos",
        },
        markers="o",
        template=TEMPLATE,
    )
    fig.add_annotation(
        text="Fonte: RAIS Estabelecimentos",
        xref="paper",
        yref="paper",
        x=0,
        y=-0.2,
        showarrow=False,
        font=dict(size=12),
    )
    fig.update_xaxes(tickmode="linear", dtick="M1", tickangle=45)
    return fig
