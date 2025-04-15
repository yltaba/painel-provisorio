from dash import dcc, html, register_page
import dash_bootstrap_components as dbc

from src.load_data import load_data
from src.utils import get_options_dropdown, create_info_popover, botao_voltar

################################ TRABALHO E RENDA #################################

register_page(__name__, path="/trabalho_renda", name="Trabalho e Renda")

# CARREGAR DADOS
all_data = load_data()

all_data["rais_anual"]["descricao_secao_cnae"] = all_data["rais_anual"][
    "descricao_secao_cnae"
].str.capitalize()
all_data["caged_media_idade"]["cnae_2_descricao_secao"] = all_data["caged_media_idade"][
    "cnae_2_descricao_secao"
].str.capitalize()
all_data["caged_media_salario"]["cnae_2_descricao_secao"] = all_data[
    "caged_media_salario"
]["cnae_2_descricao_secao"].str.capitalize()
all_data["caged_saldo_anual"]["cnae_2_descricao_secao"] = all_data["caged_saldo_anual"][
    "cnae_2_descricao_secao"
].str.capitalize()


# LISTAS PARA DROPDOWN
opcoes_cnae = get_options_dropdown(
    all_data, "caged_saldo_anual", "cnae_2_descricao_secao"
)
opcoes_cnae_rais = get_options_dropdown(all_data, "rais_anual", "descricao_secao_cnae")
opcoes_caged_ano = get_options_dropdown(all_data, "caged_saldo_secao", "ano")
opcoes_caged_ano_idade = get_options_dropdown(all_data, "caged_saldo_idade", "ano")
opcoes_cnae_caged_media_idade = get_options_dropdown(
    all_data, "caged_media_idade", "cnae_2_descricao_secao"
)
opcoes_cnae_caged_salario = get_options_dropdown(
    all_data, "caged_media_salario", "cnae_2_descricao_secao"
)

# GRÁFICOS
fig_estoque_ano = dbc.Col(
    html.Div(
        [
            html.Label("Selecione uma Seção da CNAE:"),
            dcc.Dropdown(
                id="filtro-cnae-rais-saldo",
                options=[{"label": "Todos", "value": "Todos"}] + opcoes_cnae_rais,
                value="Todos",
                clearable=False,
                className="mb-3",
            ),
            dcc.Graph(id="fig-rais-anual", config={"displayModeBar": False}),
        ]
    ),
    width=9,
)

card_estoque_atual = html.Div(
    [
        html.Div(
            [
                html.H5("Total de postos de trabalho", className="card-title"),
                html.Div(
                    [html.Div(id="card-estoque-atual-value", className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

card_variacao_estoque = html.Div(
    [
        html.Div(
            [
                html.H5("Variação %", className="card-title"),
                html.P(
                    "2022, 2023",
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
                                html.Div(
                                    id="card-variacao-estoque-value",
                                    className="card-value",
                                ),
                                html.Span(
                                    id="card-variacao-arrow",
                                    style={"fontSize": "24px", "marginLeft": "8px"},
                                ),
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

coluna_fig_estoque_ano = dbc.Col(
    [
        html.Br(),
        card_estoque_atual,
        html.Div(style={"height": "20px"}),
        card_variacao_estoque,
    ],
    width=3,
    className="cards-container",
)
cartoes_estoque_ano = html.Div(
    [
        dbc.Row(
            [
                html.H4("Estoque de postos de trabalho por ano"),
                create_info_popover(
                    "info-estoque-ano",
                    "O estoque de postos de trabalho por ano é uma métrica que mostra o estoque de postos de trabalho por ano em um determinado período.",
                ),
                coluna_fig_estoque_ano,
                fig_estoque_ano,
            ],
            className="main-content-row",
        )
    ],
    className="section-container",
    style={"marginBottom": "3rem"},
)


# Gráfico do saldo de movimentações por ano
fig_saldo_mov_ano = dbc.Col(
    html.Div(
        [
            html.Label("Selecione uma Seção da CNAE:"),
            dcc.Dropdown(
                id="filtro-cnae-caged-saldo",
                options=[{"label": "Todos", "value": "Todos"}] + opcoes_cnae,
                value="Todos",
                clearable=False,
                className="mb-3",
            ),
            dcc.Graph(id="fig-saldo-anual", config={"displayModeBar": False}),
        ]
    ),
    width=9,
)

# cards de movimentações por ano
card_saldo_atual = html.Div(
    [
        html.Div(
            [
                html.H5("Saldo de movimentações", className="card-title"),
                html.Div(
                    [html.Div(id="card-saldo-atual-value", className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

card_variacao_saldo = html.Div(
    [
        html.Div(
            [
                html.H5("Variação %", className="card-title"),
                html.P(
                    "2024, 2025",
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
                                html.Div(
                                    id="card-variacao-saldo-value",
                                    className="card-value",
                                ),
                                html.Span(
                                    id="card-variacao-saldo-arrow",
                                    style={"fontSize": "24px", "marginLeft": "8px"},
                                ),
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

coluna_fig_saldo_ano = dbc.Col(
    [
        html.Br(),
        card_saldo_atual,
        html.Div(style={"height": "20px"}),
        card_variacao_saldo,
    ],
    width=3,
    className="cards-container",
)
cartoes_saldo_ano = html.Div(
    [
        dbc.Row(
            [
                html.H4("Saldo de movimentações por ano"),
                create_info_popover(
                    "info-saldo-ano",
                    "O saldo de movimentações por ano é uma métrica que mostra o saldo de movimentações por ano em um determinado período.",
                ),
                coluna_fig_saldo_ano,
                fig_saldo_mov_ano,
            ],
            className="main-content-row",
        )
    ],
    className="section-container",
    style={"marginBottom": "3rem"},
)


# Gráfico de mov por seção da cnae
fig_saldo_mov_secao = html.Div(
    [
        html.H4("Saldo de postos de trabalho por Seção da CNAE"),
        create_info_popover(
            "info-saldo-secao",
            "O saldo de postos de trabalho por seção da CNAE é uma métrica que mostra o saldo de postos de trabalho por seção da CNAE em um determinado período.",
        ),
        html.Div(
            [
                html.Label("Selecione um ano:", style={"fontWeight": "light"}),
                dcc.Slider(
                    id="filtro-ano-caged-secao",
                    min=min(all_data["caged_saldo_secao"]["ano"]),
                    max=max(all_data["caged_saldo_secao"]["ano"]),
                    value=2025,
                    marks={
                        str(year): str(year)
                        for year in all_data["caged_saldo_secao"]["ano"].unique()
                    },
                    step=None,
                    className="mb-3",
                    updatemode="drag",
                    included=False,
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                dcc.Graph(id="fig-caged-saldo-secao"),
            ]
        ),
    ],
    className="section-container",
    style={"marginBottom": "3rem"},
)

fig_saldo_mov_idade = html.Div(
    [
        html.H4("Saldo de postos de trabalho por idade"),
        create_info_popover(
            "info-saldo-idade",
            "O saldo de postos de trabalho por idade é uma métrica que mostra o saldo de postos de trabalho por idade em um determinado período.",
        ),
        html.Div(
            [
                html.Label("Selecione um ano:", style={"fontWeight": "light"}),
                dcc.Slider(
                    id="filtro-ano-caged-idade",
                    min=min(all_data["caged_saldo_idade"]["ano"]),
                    max=max(all_data["caged_saldo_idade"]["ano"]),
                    value=2025,
                    marks={
                        str(year): str(year)
                        for year in all_data["caged_saldo_idade"]["ano"].unique()
                    },
                    step=None,
                    className="mb-3",
                    updatemode="drag",
                    included=False,
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                dcc.Graph(id="fig-caged-saldo-idade"),
            ]
        ),
    ],
    className="section-container",
    style={"marginBottom": "3rem"},
)

fig_media_salario_mov = html.Div(
    [
        html.H4("Evolução da média salarial de admissões e demissões"),
        create_info_popover(
            "info-media-salario",
            "A média salarial de admissões e demissões é uma métrica que mostra a média salarial dos funcionários que foram admitidos e demitidos.",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(
                            "Selecione uma Seção da CNAE:",
                            style={"fontWeight": "light"},
                        ),
                        dcc.Dropdown(
                            id="filtro-ano-caged-salario-medio",
                            options=[{"label": "Todos", "value": "Todos"}]
                            + opcoes_cnae_caged_salario,
                            value="Todos",
                            clearable=False,
                            className="mb-3",
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Label(
                            "Métrica:",
                            style={
                                "fontWeight": "light",
                                "textAlign": "center",
                                "width": "100%",
                            },
                        ),
                        dcc.RadioItems(
                            id="salario-stat-type",
                            options=[
                                {"label": " Média", "value": "mean"},
                                {"label": " Mediana", "value": "median"},
                            ],
                            value="mean",
                            inline=True,
                            className="mb-3",
                            style={
                                "marginTop": "8px",
                                "display": "flex",
                                "justifyContent": "center",
                                "gap": "20px",
                            },
                        ),
                    ],
                    width=6,
                    style={"paddingLeft": "20px"},
                ),
            ]
        ),
        dcc.Graph(id="fig-caged-salario-medio"),
    ],
    className="section-container",
    style={"marginBottom": "3rem"},
)

fig_media_idade_mov = html.Div(
    [
        html.H4("Evolução da média de idade das admissões e demissões"),
        create_info_popover(
            "info-media-idade",
            "A média de idade das admissões e demissões é uma métrica que mostra a idade média dos funcionários que foram admitidos e demitidos.",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(
                            "Selecione uma Seção da CNAE:",
                            style={"fontWeight": "light"},
                        ),
                        dcc.Dropdown(
                            id="filtro-ano-caged-media-idade",
                            options=[{"label": "Todos", "value": "Todos"}]
                            + opcoes_cnae_caged_media_idade,
                            value="Todos",
                            clearable=False,
                            className="mb-3",
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Label(
                            "Métrica:",
                            style={
                                "fontWeight": "light",
                                "textAlign": "center",
                                "width": "100%",
                            },
                        ),
                        dcc.RadioItems(
                            id="media-idade-stat-type",
                            options=[
                                {"label": " Média", "value": "mean"},
                                {"label": " Mediana", "value": "median"},
                            ],
                            value="mean",
                            inline=True,
                            className="mb-3",
                            style={
                                "marginTop": "8px",
                                "display": "flex",
                                "justifyContent": "center",
                                "gap": "20px",
                            },
                        ),
                    ],
                    width=6,
                    style={"paddingLeft": "20px"},
                ),
            ]
        ),
        dcc.Graph(id="fig-caged-media-idade"),
    ],
    className="section-container",
    style={"marginBottom": "3rem"},
)

layout = html.Div(
    # BOTÃO VOLTAR PARA PÁGINA INICIAL
    [
        botao_voltar(),
        # CARTÕES E GRÁFICOS
        cartoes_estoque_ano,
        cartoes_saldo_ano,
        fig_saldo_mov_secao,
        fig_saldo_mov_idade,
        fig_media_salario_mov,
        fig_media_idade_mov,
    ]
)
