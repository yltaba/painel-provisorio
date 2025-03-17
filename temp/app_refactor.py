import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pathlib import Path
import plotly.express as px
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
TEMPLATE = "plotly_white"

# DADOS
data_path = Path().resolve() / "data"

rais_anual = pd.read_csv("data/rais_anual.csv", sep=";")

caged_saldo_anual = pd.read_csv(
    "data/caged_saldo_movimentacao_anual.csv", encoding="latin1", sep=";"
)
caged_saldo_secao = pd.read_csv(
    data_path / "caged_saldo_secao.csv", sep=";", encoding="latin1"
)
caged_saldo_idade = pd.read_csv(
    "data/caged_saldo_idade.csv", sep=";", encoding="latin1"
)
caged_media_idade = pd.read_csv(
    "data/caged_media_idade.csv", sep=";", encoding="latin1"
)
caged_media_salario = pd.read_csv(
    "data/caged_media_salario.csv", sep=";", encoding="latin1"
)
pib_por_categoria = pd.read_csv(
    data_path / "pib_por_categoria.csv", sep=";", encoding="latin1"
)
pib_participacao_sp = pd.read_csv(
    data_path / "pib_participacao_sp.csv", sep=";", encoding="latin1"
)
pib_per_capita = pd.read_csv(
    data_path / "pib_per_capita.csv", sep=";", encoding="latin1"
)


# LISTAS PARA DROPDOWN
opcoes_cnae = [
    {"label": x, "value": x}
    for x in sorted(caged_saldo_anual["cnae_2_descricao_secao"].dropna().unique())
]
opcoes_cnae_rais = [
    {"label": x, "value": x}
    for x in sorted(rais_anual["descricao_secao_cnae"].dropna().unique())
]
opcoes_caged_ano = [
    {"label": x, "value": x}
    for x in sorted(caged_saldo_secao["ano"].dropna().unique(), reverse=True)
]
opcoes_caged_ano_idade = [
    {"label": x, "value": x}
    for x in sorted(caged_saldo_idade["ano"].dropna().unique(), reverse=True)
]
opcoes_cnae_caged_media_idade = [
    {"label": x, "value": x}
    for x in sorted(caged_media_idade["cnae_2_descricao_secao"].dropna().unique())
]
opcoes_cnae_caged_salario = [
    {"label": x, "value": x}
    for x in sorted(caged_media_salario["cnae_2_descricao_secao"].dropna().unique())
]


# COMPONENTES APP

# Gráficos PIB (estáticos)
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

fig_pib_per_capita = px.area(
    pib_per_capita,
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
    pib_participacao_sp,
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

# Card PIB
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

cartoes_pib = dbc.Row(
    [
        dbc.Col(card_pib_corrente, width=3),
        dbc.Col(card_variacao_pib, width=3),
    ],
    justify="left"
)

# Logo Osasco
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

# Tab economia
tab_economia = html.Div(
    [
        # PIB
        html.Br(),
        html.H4("PIB de Osasco (em R$ de 2021)"),
        html.Br(),
        cartoes_pib,
        html.Br(),
        dcc.Graph(id="fig-pib-categorias", figure=fig_pib_categorias),
        html.Br(),
        html.H4("PIB per capita - Osasco (em R$ de 2021)"),
        dcc.Graph(id="fig-pib-per-capita", figure=fig_pib_per_capita),
        html.Br(),
        html.H4("Participação do PIB de Osasco no Estado de São Paulo (em R$ de 2021)"),
        dcc.Graph(id="fig-pib-sp", figure=fig_pib_sp),
    ]
)


# Tab trabalho e renda
fig_estoque_ano = html.Div(
    [
        html.H4("Estoque de postos de trabalho por ano"),
        html.Label("Selecione uma Seção da CNAE:"),
        dcc.Dropdown(
            id="filtro-cnae-rais-saldo",
            options=[{"label": "Todos", "value": "Todos"}] + opcoes_cnae_rais,
            value="Todos",
            clearable=False,
            className="mb-3",
        ),
        dcc.Graph(id="fig-rais-anual"),
    ]
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
            value="Todos",
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
            value="Todos",
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
        html.Br(),
        fig_estoque_ano,
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

# Tab desenvolvimento urbano
tab_desenvolvimento_urbano = html.Div(
    [
        html.Br(),
        html.H4("Zoneamento de Osasco"),
        html.Iframe(
            src="https://ozmundi.osasco.sp.gov.br/misc/base_zoneamento/",
            style={
                "width": "100%",
                "height": "500px",
                "border": "none",
            },
        ),
    ]
)

# Consolidação Tabs
all_tabs = dcc.Tabs(
            id="tabs",
            value="home",
            children=[
                dcc.Tab(label="Home", value="home"),
                dcc.Tab(label="Desenvolvimento Econômico", value="economia"),
                dcc.Tab(label="Trabalho e Renda", value="trabalho"),
                dcc.Tab(label="Desenvolvimento Urbano", value="urbano"),
            ],
)


# APP LAYOUT
external_stylesheets = [dbc.themes.MORPH]
app = dash.Dash(
    external_stylesheets=external_stylesheets, suppress_callback_exceptions=True
)

app.layout = dbc.Container(
    [
        imagem_cabecalho,
        html.Br(),
        all_tabs,
        html.Div(id="tabs-content"),
    ]
)

@app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "economia":
        return tab_economia

    elif tab == "trabalho":
        return tab_trabalho_renda

    elif tab == "urbano":
        return tab_desenvolvimento_urbano
    return html.Div(
        [html.Br(), html.H4("Bem-vindo ao Painel de Governo da Prefeitura de Osasco")]
    )


# CALLBACKS DE FILTRO - GRÁFICOS
@app.callback(
    Output("fig-rais-anual", "figure"), Input("filtro-cnae-rais-saldo", "value")
)
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
        template="plotly_white",
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


@app.callback(
    Output("fig-saldo-anual", "figure"), Input("filtro-cnae-caged-saldo", "value")
)
def atualizar_grafico_caged(filtro_cnae):
    if filtro_cnae == "Todos":
        df_filtrado = caged_saldo_anual
    else:
        df_filtrado = caged_saldo_anual[
            caged_saldo_anual["cnae_2_descricao_secao"] == filtro_cnae
        ]

    caged_ano = df_filtrado.groupby("ano", as_index=False).agg(
        {"saldo_movimentacao": "sum"}
    )

    fig = px.bar(
        caged_ano,
        x="ano",
        y="saldo_movimentacao",
        template=TEMPLATE,
        labels={
            "ano": "Ano",
            "saldo_movimentacao": "Saldo das movimentações",
        },
    )
    fig.add_annotation(
        text="Fonte: CAGED e NOVO CAGED",
        xref="paper",
        yref="paper",
        x=0,
        y=-0.2,
        showarrow=False,
        font=dict(size=12),
    )
    fig.update_xaxes(tickmode="linear", dtick="M1", tickangle=45)
    return fig


@app.callback(
    Output("fig-caged-saldo-secao", "figure"), Input("filtro-ano-caged-secao", "value")
)
def atualizar_grafico_caged_saldo_secao(filtro_ano):
    if filtro_ano == "Todos":
        df_filtrado = caged_saldo_secao
    else:
        df_filtrado = caged_saldo_secao[caged_saldo_secao["ano"] == filtro_ano]

    caged_saldo_secao_grp = (
        df_filtrado.groupby("cnae_2_descricao_secao", as_index=False)
        .agg({"saldo_movimentacao": "sum"})
        .sort_values("saldo_movimentacao")
    )

    fig = px.bar(
        caged_saldo_secao_grp,
        x="saldo_movimentacao",
        y="cnae_2_descricao_secao",
        orientation="h",
        labels={
            "saldo_movimentacao": "Saldo das movimentações",
            "cnae_2_descricao_secao": "Seção da CNAE",
        },
        template=TEMPLATE,
    )
    fig.add_annotation(
        text="Fonte: CAGED e NOVO CAGED",
        xref="paper",
        yref="paper",
        x=0.0,
        y=-0.2,
        showarrow=False,
        font=dict(size=12),
        xanchor="center",
    )
    return fig


@app.callback(
    Output("fig-caged-saldo-idade", "figure"), Input("filtro-ano-caged-idade", "value")
)
def atualizar_grafico_caged_saldo_idade(filtro_ano):
    if filtro_ano == "Todos":
        df_filtrado = caged_saldo_idade
    else:
        df_filtrado = caged_saldo_idade[caged_saldo_idade["ano"] == filtro_ano]

    caged_saldo_idade_grp = (
        df_filtrado.groupby("idade", as_index=False)
        .agg({"saldo_movimentacao": "sum"})
        .sort_values("saldo_movimentacao")
    )

    fig = px.bar(
        caged_saldo_idade_grp,
        x="saldo_movimentacao",
        y="idade",
        labels={
            "idade": "Idade",
            "saldo_movimentacao": "Saldo das movimentações",
        },
        orientation="h",
        template=TEMPLATE,
    )
    fig.add_annotation(
        text="Fonte: CAGED e NOVO CAGED",
        xref="paper",
        yref="paper",
        x=0.05,
        y=-0.2,
        showarrow=False,
        font=dict(size=12),
        xanchor="center",
    )
    return fig


@app.callback(
    Output("fig-caged-salario-medio", "figure"),
    Input("filtro-ano-caged-salario-medio", "value"),
)
def atualizar_grafico_caged_media_salario(filtro_cnae):
    # Filtrar por CNAE, se aplicável
    df_filtrado = (
        caged_media_salario
        if filtro_cnae == "Todos"
        else caged_media_salario[
            caged_media_salario["cnae_2_descricao_secao"] == filtro_cnae
        ]
    )

    # Agrupar corretamente
    caged_media_salario_grp = (
        df_filtrado.groupby(["ano", "variable"], as_index=False)
        .agg(salario_medio=("salario_medio", "mean"))  # Evita dicionário dentro do agg
        .sort_values("ano")  # Garante ordenação correta para o gráfico
    )

    # Criar gráfico de linha
    fig = px.line(
        caged_media_salario_grp,
        y="salario_medio",
        x="ano",
        labels={
            "ano": "Ano",
            "salario_medio": "Média Salarial",
        },
        color="variable",
        markers=True,
        template=TEMPLATE,
    )

    # Adicionar anotação da fonte
    fig.add_annotation(
        text="Fonte: CAGED e NOVO CAGED",
        xref="paper",
        yref="paper",
        x=0.0,
        y=-0.2,
        showarrow=False,
        font=dict(size=12),
        xanchor="left",
    )

    return fig


@app.callback(
    Output("fig-caged-media-idade", "figure"),
    Input("filtro-ano-caged-media-idade", "value"),
)
def atualizar_grafico_caged_media_idade(filtro_cnae):
    # Filtrar por CNAE, se aplicável
    df_filtrado = (
        caged_media_idade
        if filtro_cnae == "Todos"
        else caged_media_idade[
            caged_media_idade["cnae_2_descricao_secao"] == filtro_cnae
        ]
    )

    # Agrupar corretamente
    caged_media_idade_grp = (
        df_filtrado.groupby(["ano", "variable"], as_index=False)
        .agg(media_idade=("media_idade", "mean"))  # Evita dicionário dentro do agg
        .sort_values("ano")  # Garante ordenação correta para o gráfico
    )

    # Criar gráfico de linha
    fig = px.line(
        caged_media_idade_grp,
        y="media_idade",
        x="ano",
        labels={
            "ano": "Ano",
            "media_idade": "Média de Idade",
        },
        color="variable",
        markers=True,
        template=TEMPLATE,
    )

    # Adicionar anotação da fonte
    fig.add_annotation(
        text="Fonte: CAGED e NOVO CAGED",
        xref="paper",
        yref="paper",
        x=0.0,
        y=-0.2,
        showarrow=False,
        font=dict(size=12),
        xanchor="left",
    )

    return fig


server = app.server
if __name__ == "__main__":
    app.run_server(debug=True)
