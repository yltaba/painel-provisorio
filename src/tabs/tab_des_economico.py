from dash import dcc, html
import dash_bootstrap_components as dbc
import locale
import plotly.express as px

from src.utils import create_card_valor, calcular_pib_atual, calcular_variacao_pib
from src.config import TEMPLATE
from src.load_data import load_data


################################ DESENVOLVIMENTO ECONÔMICO #################################
# CARREGAR DADOS
all_data = load_data()

# GRÁFICOS PIB
def get_pib_plots(all_data):

    # COMPONENTES APP
    # Gráficos PIB (estáticos)
    fig_pib_categorias = px.line(
        all_data["pib_por_categoria"],
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

    fig_pib_per_capita = px.area(
        all_data["pib_per_capita"],
        x="ano",
        y="pib_per_capita",
        labels={
            "ano": "Ano",
            "pib_per_capita": "PIB per capita",
        },
        markers=True,
        template=TEMPLATE,
    )
    fig_pib_per_capita.update_xaxes(tickmode="linear", tickangle=45)

    fig_pib_sp = px.area(
        all_data['pib_participacao_sp'],
        x="ano",
        y="participacao_pib_sp",
        labels={
            "ano": "Ano",
            "participacao_pib_sp": "Participação % de Osasco no PIB de SP",
        },
        markers=True,
        template=TEMPLATE,
    )
    fig_pib_sp.update_xaxes(tickmode="linear", tickangle=45)
    fig_pib_sp.update_layout(
        yaxis_tickformat=".1%",
    )
    for fig in [fig_pib_sp, fig_pib_per_capita, fig_pib_categorias]:
        fig.add_annotation(
            text="Fonte: IBGE",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="center",
        )
    return fig_pib_sp, fig_pib_per_capita, fig_pib_categorias
fig_pib_sp, fig_pib_per_capita, fig_pib_categorias = get_pib_plots(all_data)

# VALORES PIB PARA CARD LATERAL
pib_corrente = calcular_pib_atual(all_data["pib_por_categoria"])
variacao_pib = calcular_variacao_pib(all_data["pib_por_categoria"])

card_pib_corrente = create_card_valor(
    f"PIB {all_data['pib_por_categoria']['ano'].max()}", pib_corrente, currency=True
)
card_variacao_pib = create_card_valor("Crescimento %", variacao_pib)

coluna_cartao_pib_categorias = dbc.Col(
    [
        card_pib_corrente,
        html.Div(style={"height": "20px"}),  # Spacer between cards
        card_variacao_pib,
    ],
    width=3,
    className="cards-container",
)

cartoes_pib_categorias = dbc.Row(
    [
        coluna_cartao_pib_categorias,
        dbc.Col(
            dcc.Graph(
                id="pib-graph",
                figure=fig_pib_categorias,
                config={"displayModeBar": False},
            ),
            width=9,
        ),
    ],
    className="main-content-row",
)

# VALORES PIB PER CAPITA PARA CARD LATERAL
vl_pib_per_capita = all_data["pib_per_capita"].loc[
    all_data["pib_per_capita"]["ano"] == all_data["pib_per_capita"]["ano"].max()
]["pib_per_capita"].values[0]
# vl_pib_per_capita = locale.format_string("%.1f", vl_pib_per_capita, grouping=True)

card_pib_per_capita = create_card_valor(
    f"PIB per capita {all_data["pib_per_capita"]['ano'].max()}", vl_pib_per_capita, currency=True
)

# VALORES POPULAÇÃO PARA CARD LATERAL
vl_populacao = all_data["pib_per_capita"].loc[
    all_data["pib_per_capita"]["ano"] == all_data["pib_per_capita"]["ano"].max()
]["populacao"].values[0]
# vl_populacao = locale.format_string("%.0f", vl_populacao, grouping=True)

card_populacao = create_card_valor(
    f"População {all_data['pib_per_capita']['ano'].max()}", vl_populacao
)

coluna_cartao_pib_per_capita = dbc.Col(
    [
        card_pib_per_capita,
        html.Div(style={"height": "20px"}),
        card_populacao,
    ],
    width=3,
    className="cards-container",
)

cartoes_pib_per_capita = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="pib-per-capita-graph",
                figure=fig_pib_per_capita,
                config={"displayModeBar": False},
            ),
            width=9,
        ),
        coluna_cartao_pib_per_capita,
    ],
    className="main-content-row",
)

# TAB ECONOMIA
tab_economia = html.Div(
    [
        # PIB
        html.Br(),
        html.H4("PIB (em R$ de 2021)"),
        cartoes_pib_categorias,
        html.Br(),
        html.H4("PIB per capita (em R$ de 2021)"),
        cartoes_pib_per_capita,
        html.Br(),
        html.H4("Participação do PIB de Osasco no Estado de São Paulo"),
        dcc.Graph(id="fig-pib-sp", figure=fig_pib_sp, config={"displayModeBar": False}),
    ]
)