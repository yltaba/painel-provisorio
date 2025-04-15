from dash import dcc, html, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
from babel.numbers import format_decimal, format_currency

from src.utils import (
    calcular_pib_atual,
    calcular_variacao_pib,
    create_info_popover,
    get_options_dropdown,
)
from src.config import TEMPLATE
from src.load_data import load_data


register_page(
    __name__, path="/desenvolvimento_economico", name="Desenvolvimento Econômico"
)

################################ DESENVOLVIMENTO ECONÔMICO #################################
# CARREGAR DADOS
all_data = load_data()


# GRÁFICOS PIB
def get_pib_plots(all_data):

    # GRÁFICO PIB POR CATEGORIA
    df_pib_categorias = (
        all_data["pib_por_categoria"]
        .loc[all_data["pib_por_categoria"]["variavel_dash"] != "Total"]
        .copy()
    )
    fig_pib_categorias = px.bar(
        df_pib_categorias,
        x="ano",
        y="pib_deflacionado",
        color="variavel_dash",
        color_discrete_sequence=[
            "#1666ba",
            "#368ce7",
            "#7ab3ef",
            "#bedaf7",
            "#deecfb",
        ],
        labels={
            "ano": "Ano",
            "pib_deflacionado": "PIB (deflacionado)",
            "variavel_dash": "Categoria",
        },
        template=TEMPLATE,
    )
    fig_pib_categorias.update_xaxes(tickmode="linear", tickangle=45)
    fig_pib_categorias.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="white",
            bordercolor="lightgray",
        ),
    )
    fig_pib_categorias.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Ano: %{x}<br>PIB: R$ %{y:,.2f}<extra></extra>"
    )

    # GRÁFICO PIB PER CAPITA
    fig_pib_per_capita = px.line(
        all_data["pib_per_capita"],
        x="ano",
        y="pib_per_capita",
        color="municipio",
        line_shape="spline",
        labels={
            "ano": "Ano",
            "pib_per_capita": "PIB per capita (R$)",
            "municipio": "Município",
        },
        template="none",
    )

    fig_pib_per_capita.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(tickformat=",.0f", gridcolor="lightgray", zeroline=False),
        xaxis=dict(gridcolor="white", zeroline=False),
        legend_title_text="Município",
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5
        ),
    )

    fig_pib_per_capita.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2.5 if trace.name == "Osasco (SP)" else 1.5,
                dash="solid" if trace.name == "Osasco (SP)" else "dash",
            ),
            marker=dict(size=8 if trace.name == "Osasco (SP)" else 6),
            opacity=1 if trace.name == "Osasco (SP)" else 0.75,
        )
    )
    fig_pib_per_capita.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Ano: %{x}<br>PIB per capita: R$ %{y:,.2f}<extra></extra>"
    )
    fig_pib_per_capita.update_xaxes(tickmode="linear", tickangle=45)

    # GRÁFICO PARTICIPAÇÃO DO PIB MUNICIPAL NO PIB DE SÃO PAULO
    fig_pib_sp = px.line(
        all_data["pib_participacao_sp"],
        x="ano",
        y="participacao_pib_sp",
        color="municipio",
        line_shape="spline",
        labels={
            "ano": "Ano",
            "participacao_pib_sp": "Participação % PIB de SP",
            "municipio": "Município",
        },
        template="none",
    )
    fig_pib_sp.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco (SP)" else 1.5,
                dash="solid" if trace.name == "Osasco (SP)" else "dot",
            ),
            opacity=1 if trace.name == "Osasco (SP)" else 0.7,
        )
    )
    fig_pib_sp.update_xaxes(tickmode="linear", tickangle=45)

    fig_pib_sp.update_layout(
        yaxis_tickformat=".%",
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(
            tickformat=",.1%", gridcolor="lightgray", zeroline=False, title_standoff=30
        ),
        xaxis=dict(gridcolor="white", zeroline=False),
        legend_title_text="Município",
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5
        ),
    )
    fig_pib_sp.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Ano: %{x}<br>Participação: %{y:,.2%}<extra></extra>"
    )

    # ATRIBUIR MARGEM E ANOTAÇÃO DE FONTE A TODOS OS GRÁFICOS
    for fig in [fig_pib_sp, fig_pib_per_capita, fig_pib_categorias]:
        fig.update_layout(
            margin=dict(t=0),
        )
        fig.add_annotation(
            text="Fonte: <a href='https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html'>IBGE</a>",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="center",
            clicktoshow=False,
        )
    return fig_pib_sp, fig_pib_per_capita, fig_pib_categorias


fig_pib_sp, fig_pib_per_capita, fig_pib_categorias = get_pib_plots(all_data)

# VALORES PIB PARA CARD LATERAL
pib_corrente = calcular_pib_atual(all_data["pib_por_categoria"])
variacao_pib = calcular_variacao_pib(all_data["pib_por_categoria"])

card_pib_corrente = html.Div(
    [
        html.Div(
            [
                html.H5(
                    f"PIB {all_data['pib_por_categoria']['ano'].max()}",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(pib_corrente, className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

arrow_symbol = "▲" if float(variacao_pib.strip("%").replace(",", ".")) >= 0 else "▼"
arrow_style = {
    "color": (
        "#28a745"
        if float(variacao_pib.strip("%").replace(",", ".")) >= 0
        else "#dc3545"
    ),
    "fontSize": "24px",
    "marginLeft": "8px",
}

card_variacao_pib = html.Div(
    [
        html.Div(
            [
                html.H5("Variação %", className="card-title"),
                html.P(
                    "2020, 2021",
                    className="card-subtitle",
                    style={
                        "fontSize": "12px",
                        "textAlign": "center",
                        "color": "#6c757d",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(variacao_pib, className="card-value"),
                                html.Span(arrow_symbol, style=arrow_style),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                            },
                        )
                    ],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)


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
vl_pib_per_capita = (
    all_data["pib_per_capita"]
    .loc[all_data["pib_per_capita"]["ano"] == all_data["pib_per_capita"]["ano"].max()][
        "pib_per_capita"
    ]
    .values[0]
)

vl_pib_per_capita = format_currency(
    vl_pib_per_capita, "BRL", locale="pt_BR", currency_digits=False
)

card_pib_per_capita = html.Div(
    [
        html.Div(
            [
                html.H5(
                    f"PIB per capita {all_data['pib_por_categoria']['ano'].max()}",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(vl_pib_per_capita, className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

# VALORES POPULAÇÃO PARA CARD LATERAL
vl_populacao = (
    all_data["pib_per_capita"]
    .loc[all_data["pib_per_capita"]["ano"] == all_data["pib_per_capita"]["ano"].max()][
        "populacao"
    ]
    .values[0]
)

vl_populacao = format_decimal(vl_populacao, format="#,##0", locale="pt_BR")

card_populacao = html.Div(
    [
        html.Div(
            [
                html.H5(
                    f"População {all_data['pib_per_capita']['ano'].max()}",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(vl_populacao, className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
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
        coluna_cartao_pib_per_capita,
        dbc.Col(
            dcc.Graph(
                id="pib-per-capita-graph",
                figure=fig_pib_per_capita,
                config={"displayModeBar": False},
            ),
            width=9,
        ),
    ],
    className="main-content-row",
)


# ABERTURA E ENCERRAMENTO DE EMPRESAS
opcoes_des_atividade = get_options_dropdown(
    all_data, "abertura_encerramento_empresas_cleaned", "des_atividade"
)

dropdown_des_atividade = dcc.Dropdown(
    id="filtro-des-atividade",
    options=[{"label": "Todos", "value": "Todos"}] + opcoes_des_atividade,
    value="Todos",
    clearable=False,
    className="mb-3",
)

fig_empresas_ano = dbc.Col(
    html.Div(
        [
            dropdown_des_atividade,
            dcc.Graph(id="fig-abertura-encerramento", config={"displayModeBar": False}),
        ]
    ),
    width=9,
)

saldo_empresas = (
    all_data["abertura_encerramento_empresas_cleaned"]
    .loc[
        all_data["abertura_encerramento_empresas_cleaned"]["ano"]
        == all_data["abertura_encerramento_empresas_cleaned"]["ano"].max()
    ]["n_empresas_abertas"]
    .sum()
)

card_saldo_empresas = html.Div(
    [
        html.Div(
            [
                html.H5(
                    f"Saldo de empresas",
                    className="card-title",
                ),
                html.P(
                    f"{all_data['abertura_encerramento_empresas_cleaned']['ano'].max()}",
                    className="card-subtitle",
                    style={
                        "fontSize": "12px",
                        "textAlign": "center",
                        "color": "#6c757d",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            id="card-saldo-empresas-value", className="card-value"
                        ),
                        html.Span(
                            id="card-variacao-saldo-empresas-arrow",
                            style={"fontSize": "24px", "marginLeft": "8px"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                    },
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

coluna_cartao_saldo_empresas = dbc.Col(
    [
        card_saldo_empresas,
        html.Div(style={"height": "20px"}),
    ],
    width=3,
    className="cards-container",
)

cartoes_abertura_encerramento = dbc.Row(
    [
        coluna_cartao_saldo_empresas,
        fig_empresas_ano,
    ],
    className="main-content-row",
)

# LAYOUT DA PÁGINA
layout = html.Div(
    [
        # PIB CATEGORIAS
        html.Br(),
        html.Div(
            [
                html.H4("PIB (em R$ de 2021)"),
                create_info_popover(
                    "info-pib",
                    "O PIB é o valor total de todos os bens e serviços produzidos em um determinado período de tempo, geralmente um ano. Ele é uma das principais medidas da atividade econômica de um país ou região.",
                ),
                cartoes_pib_categorias,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # PIB PER CAPITA
        html.Div(
            [
                html.H4("PIB per capita (em R$ de 2021)"),
                create_info_popover(
                    "info-pib-per-capita",
                    "O PIB per capita é uma medida da renda média de cada indivíduo na economia. Ele é calculado dividindo o PIB total pelo número de habitantes.",
                ),
                cartoes_pib_per_capita,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # PARTICIPAÇÃO DO PIB MUNICIPAL NO PIB DE SÃO PAULO
        html.Div(
            [
                html.H4("Participação do PIB municipal no Estado de São Paulo"),
                create_info_popover(
                    "info-pib-sp",
                    "A participação do PIB de Osasco no Estado de São Paulo é uma medida da proporção do PIB de Osasco em relação ao PIB total do Estado de São Paulo. Ela é calculada dividindo o PIB de Osasco pelo PIB total do Estado de São Paulo.",
                ),
                dcc.Graph(
                    id="fig-pib-sp", figure=fig_pib_sp, config={"displayModeBar": False}
                ),
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # ABERTURA E ENCERRAMENTO DE EMPRESAS
        html.Div(
            [
                html.H4("Abertura e encerramento de empresas"),
                create_info_popover(
                    "info-abertura-encerramento",
                    "Abertura e encerramento de empresas do SIGT.",
                ),
                cartoes_abertura_encerramento,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
    ]
)
