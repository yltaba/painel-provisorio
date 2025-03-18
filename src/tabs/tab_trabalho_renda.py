from dash import dcc, html
import dash_bootstrap_components as dbc
from babel.numbers import format_percent

from src.load_data import load_data
from src.utils import get_options_dropdown
################################ TRABALHO E RENDA #################################

# CARREGAR DADOS
all_data = load_data()


# LISTAS PARA DROPDOWN
opcoes_cnae = get_options_dropdown(all_data, "caged_saldo_anual", "cnae_2_descricao_secao")
opcoes_cnae_rais = get_options_dropdown(all_data, "rais_anual", "descricao_secao_cnae")
opcoes_caged_ano = get_options_dropdown(all_data, "caged_saldo_secao", "ano")
opcoes_caged_ano_idade = get_options_dropdown(all_data, "caged_saldo_idade", "ano")
opcoes_cnae_caged_media_idade = get_options_dropdown(all_data, "caged_media_idade", "cnae_2_descricao_secao")
opcoes_cnae_caged_salario = get_options_dropdown(all_data, "caged_media_salario", "cnae_2_descricao_secao")

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

# Create cards with static titles and dynamic value containers
card_estoque_atual = html.Div([
    html.Div([  # Add a container div for vertical centering
        html.H5("Total de postos de trabalho", className="card-title"),
        html.Div([
            html.Div(id="card-estoque-atual-value", className="card-value")
        ], className="card-value-container")
    ], className="card-content")
], className="custom-card")

card_variacao_estoque = html.Div([
    html.Div([  # Add a container div for vertical centering
        html.H5("Variação %", className="card-title"),
        html.Div([
            html.Div(id="card-variacao-estoque-value", className="card-value")
        ], className="card-value-container")
    ], className="card-content")
], className="custom-card")

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
cartoes_estoque_ano = dbc.Row(
    [
        html.H4("Estoque de postos de trabalho por ano"),
        coluna_fig_estoque_ano,
        fig_estoque_ano,
    ],
    className="main-content-row",
)

fig_saldo_mov_ano = html.Div(
    [
        html.H4("Saldo de movimentações por ano"),
        html.Label("Selecione uma Seção da CNAE:", style={"fontWeight": "light"}),
        dcc.Dropdown(
            id="filtro-cnae-caged-saldo",
            options=[{"label": "Todos", "value": "Todos"}] + opcoes_cnae,
            value="Todos",
            clearable=False,
            className="mb-3",
        ),
        dcc.Graph(id="fig-saldo-anual"),
    ]
)


fig_saldo_mov_secao = html.Div(
    [
        html.H4("Saldo de postos de trabalho por Seção da CNAE"),
        html.Label("Selecione um ano:", style={"fontWeight": "light"}),
        dcc.Dropdown(
            id="filtro-ano-caged-secao",
            options=[{"label": "Todos", "value": "Todos"}] + opcoes_caged_ano,
            value=2024,
            clearable=False,
            className="mb-3",
        ),
        dcc.Graph(id="fig-caged-saldo-secao"),
    ]
)

fig_saldo_mov_idade = html.Div(
    [
        html.H4("Saldo de postos de trabalho por idade"),
        html.Label("Selecione um ano:", style={"fontWeight": "light"}),
        dcc.Dropdown(
            id="filtro-ano-caged-idade",
            options=[{"label": "Todos", "value": "Todos"}] + opcoes_caged_ano_idade,
            value=2024,
            clearable=False,
            className="mb-3",
        ),
        dcc.Graph(id="fig-caged-saldo-idade"),
    ]
)

fig_media_salario_mov = html.Div(
    [
        html.H4("Evolução da média salarial de admissões e demissões"),
        html.Label("Selecione uma Seção da CNAE:", style={"fontWeight": "light"}),
        dcc.Dropdown(
            id="filtro-ano-caged-salario-medio",
            options=[{"label": "Todos", "value": "Todos"}] + opcoes_cnae_caged_salario,
            value="Todos",
            clearable=False,
            className="mb-3",
        ),
        dcc.Graph(id="fig-caged-salario-medio"),
    ]
)

fig_media_idade_mov = html.Div(
    [
        html.H4("Evolução da média de idade das admissões e demissões"),
        html.Label("Selecione uma Seção da CNAE:", style={"fontWeight": "light"}),
        dcc.Dropdown(
            id="filtro-ano-caged-media-idade",
            options=[{"label": "Todos", "value": "Todos"}]
            + opcoes_cnae_caged_media_idade,
            value="Todos",
            clearable=False,
            className="mb-3",
        ),
        dcc.Graph(id="fig-caged-media-idade"),
    ]
)

tab_trabalho_renda = html.Div(
    [
        cartoes_estoque_ano,
        html.Br(),
        fig_saldo_mov_ano,
        html.Br(),
        fig_saldo_mov_secao,
        html.Br(),
        fig_saldo_mov_idade,
        html.Br(),
        fig_media_salario_mov,
        html.Br(),
        fig_media_idade_mov,
        html.Br(),
    ]
)