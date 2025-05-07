from dash import html, register_page, dcc, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from babel.numbers import format_decimal, format_currency
from src.utils import create_info_popover
from src.load_data import load_data
from src.config import TEMPLATE

register_page(__name__, path="/desenvolvimento_humano", name="Desenvolvimento Humano")

all_data = load_data()

# cad_unico = all_data["cad_unico_painel"].copy()
cod_familiar_fam = all_data["cod_familiar_fam"].copy()
cod_familiar_fam_2025 = all_data["cod_familiar_fam_2025"].copy()
renda_per_capita_fam = all_data["renda_per_capita_fam"].copy()
n_pessoas_fam = all_data["n_pessoas_fam"].copy()
escoa_sanitario_fam = all_data["escoa_sanitario_fam"].copy()
agua_canalizada_fam = all_data["agua_canalizada_fam"].copy()
qtd_comodos_domic_fam = all_data["qtd_comodos_domic_fam"].copy()
df_sabe_ler_escrever = all_data["sabe_ler_escrever_memb"].copy()
df_sexo_biologico = all_data["sexo_pessoa"].copy()
df_forma_coleta = all_data["forma_coleta"].copy()
df_parentesco = all_data["parentesco"].copy()


# CARTÕES
n_familias_cadastradas = format_decimal(
    cod_familiar_fam["cod_familiar_fam"].nunique(), format="#,##0", locale="pt_BR"
)
card_n_familias_cadastradas = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Total de famílias cadastradas",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(n_familias_cadastradas, className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

n_familias_cadastradas_2025 = format_decimal(
    cod_familiar_fam_2025["cod_familiar_fam"].nunique(),
    format="#,##0",
    locale="pt_BR",
)
card_n_familias_cadastradas_2025 = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Famílias cadastradas em 2025",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(n_familias_cadastradas_2025, className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

media_renda_per_capita = format_currency(
    renda_per_capita_fam["vlr_renda_per_capita_fam"].mean(), "BRL", locale="pt_BR"
)
card_media_renda_per_capita = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Renda média per capita",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(media_renda_per_capita, className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

media_pessoas_familia = format_decimal(
    n_pessoas_fam["n_pessoas_fam"].mean(),
    format="#,##0.00",
    locale="pt_BR",
)
card_media_pessoas_familia = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Média de pessoas por família",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(media_pessoas_familia, className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

media_pessoas_domic = format_decimal(
    n_pessoas_fam["qtd_pessoas_domic_fam"].mean(),
    format="#,##0.00",
    locale="pt_BR",
)
card_media_pessoas_domic = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Média de pessoas por domicílio",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(media_pessoas_domic, className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

n_domicilios_sem_rede_esgoto = format_decimal(
    escoa_sanitario_fam["cod_familiar_fam"].nunique(), format="#,##0", locale="pt_BR"
)
card_n_domicilios_sem_rede_esgoto = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Domicílios sem rede de esgoto",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(n_domicilios_sem_rede_esgoto, className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

n_domicilios_sem_agua_canalizada = format_decimal(
    agua_canalizada_fam["cod_familiar_fam"].nunique(), format="#,##0", locale="pt_BR"
)
card_n_domicilios_sem_agua_canalizada = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Domicílios sem água canalizada",
                    className="card-title",
                ),
                html.Div(
                    [
                        html.Div(
                            n_domicilios_sem_agua_canalizada, className="card-value"
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

media_comodos_domic = format_decimal(
    qtd_comodos_domic_fam["qtd_comodos_domic_fam"].mean(),
    format="#,##0.00",
    locale="pt_BR",
)
card_media_comodos_domic = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Média de cômodos por domicílio",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(media_comodos_domic, className="card-value")],
                    className="card-value-container",
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

# CONSOLIDAÇÃO DOS CARTÕES
cards_cadastro = dbc.Row(
    [
        dbc.Col(
            card_n_familias_cadastradas,
            width=3,
        ),
        dbc.Col(
            card_n_familias_cadastradas_2025,
            width=3,
        ),
        dbc.Col(
            card_media_renda_per_capita,
            width=3,
        ),
        dbc.Col(
            card_media_pessoas_familia,
            width=3,
        ),
    ],
    className="mb-4",
)

cards_domicilio = dbc.Row(
    [
        dbc.Col(
            card_media_pessoas_domic,
            width=3,
        ),
        dbc.Col(
            card_media_comodos_domic,
            width=3,
        ),
        dbc.Col(
            card_n_domicilios_sem_agua_canalizada,
            width=3,
        ),
        dbc.Col(
            card_n_domicilios_sem_rede_esgoto,
            width=3,
        ),
    ],
    className="mb-4",
)

# GRÁFICOS

alfabet_colors = {"Masculino": "#89CFF0", "Feminino": "#FFB6C1"}
fig_sabe_ler_escrever = px.pie(
    df_sabe_ler_escrever,
    values="count",
    hole=0.5,
    names="desc_cod_sabe_ler_escrever_memb",
    color_discrete_map=alfabet_colors,
    template=TEMPLATE,
)
fig_sabe_ler_escrever.update_traces(textposition="outside", textinfo="percent+label")
fig_sabe_ler_escrever.update_layout(
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

sex_colors = {"Masculino": "#89CFF0", "Feminino": "#FFB6C1"}
fig_sexo_biologico = px.pie(
    df_sexo_biologico,
    values="count",
    hole=0.5,
    names="desc_cod_sexo_pessoa",
    color_discrete_map=sex_colors,
    template=TEMPLATE,
)
fig_sexo_biologico.update_traces(textposition="outside", textinfo="percent+label")
fig_sexo_biologico.update_layout(
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)


# figura de cadastros por ano e forma de coleta
forma_coleta_colors = {
    "Com visita domiciliar": "#1666ba",
    "Sem visita domiciliar": "#368ce7",
    "Não informado": "#7ab3ef",
}
fig_cadastro_forma_coleta = px.bar(
    df_forma_coleta,
    x="ano_cadastramento",
    y="n_familias",
    color="desc_cod_forma_coleta_fam",
    labels={
        "desc_cod_forma_coleta_fam": "Forma de coleta",
        "ano_cadastramento": "Ano de cadastro",
        "n_familias": "Número de famílias",
    },
    template=TEMPLATE,
    color_discrete_map=forma_coleta_colors,
)
fig_cadastro_forma_coleta.update_layout(
    yaxis=dict(tickformat=",.0f", gridcolor="lightgray", zeroline=False),
    xaxis=dict(tickmode="linear", tickangle=45),
)
fig_cadastro_forma_coleta.update_layout(
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor="white",
        bordercolor="lightgray",
    ),
)


row_graficos_cadastro_sexo = dbc.Row(
    [
        dbc.Col(
            [
                html.H4(
                    "Evolução de cadastros por ano e forma de coleta",
                    id="evolucao_cadastros",
                ),
                dcc.Graph(figure=fig_cadastro_forma_coleta),
            ],
            width=8,
        ),
        dbc.Col(
            [
                html.H4(
                    "Pessoas cadastradas por sexo biológico:",
                    id="sexo_biologico",
                ),
                dcc.Graph(figure=fig_sexo_biologico),
            ],
            width=4,
        ),
    ]
)


fig_parentesco = px.bar(
    df_parentesco,
    x="count",
    y="desc_cod_parentesco_rf_pessoa",
    orientation="h",
    template=TEMPLATE,
    color_discrete_sequence=["#1666ba"],
    labels={
        "desc_cod_parentesco_rf_pessoa": "Parentesco",
        "count": "Número de pessoas",
    },
)
fig_parentesco.update_layout(xaxis=dict(tickformat=",.0f"))

# Create a sample table with some of your CadÚnico data
indicadores_bairros = all_data["indicadores_bairros"].copy()

# Rename columns for better readability
column_names = {
    "bairro": "Bairro",
    "cod_familiar_fam": "Nº de Famílias",
    "vlr_renda_per_capita_fam": "Média de Renda per Capita",
    "qtd_pessoas_domic_fam": "Média de Pessoas por Domicílio",
    "qtd_comodos_domic_fam": "Média de Cômodos por Domicílio",
    "qtd_familias_domic_fam": "Média de Famílias por Domicílio",
    "val_desp_energia_fam": "Média de Despesa de Energia",
    "val_desp_agua_esgoto_fam": "Média de Despesa de Água/Esgoto",
    "val_desp_alimentacao_fam": "Média de Despesa de Alimentação",
}
indicadores_bairros = indicadores_bairros.rename(columns=column_names)

# Create the interactive table with modern styling
table = dash_table.DataTable(
    id="interactive-table",
    columns=[
        {
            "name": col,
            "id": col,
            "type": "numeric" if col != "Bairro" else "text",
            "format": (
                {
                    "locale": {"decimal": ",", "group": "."},
                    "specifier": (
                        ",.2f" if "Despesa" in col or "Renda" in col else ",.1f"
                    ),
                }
                if col != "Bairro"
                else None
            ),
        }
        for col in indicadores_bairros.columns
    ],
    data=indicadores_bairros.to_dict("records"),
    # Modern Features
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    page_size=5,
    # Styling
    style_table={
        "overflowX": "auto",
        "border": "thin lightgrey solid",
        "borderRadius": "8px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
    },
    # Cell styling
    style_cell={
        "fontFamily": 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        "textAlign": "left",
        "padding": "12px 15px",
        "backgroundColor": "white",
        "minWidth": "100px",
        "maxWidth": "300px",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
    },
    # Header styling
    style_header={
        "backgroundColor": "#f8f9fa",
        "fontWeight": "bold",
        "border": "none",
        "borderBottom": "2px solid #dee2e6",
        "textAlign": "left",
        "padding": "12px 15px",
        "whiteSpace": "normal",
    },
    # Data styling
    style_data={
        "border": "none",
        "borderBottom": "1px solid #f2f2f2",
        "whiteSpace": "normal",
        "height": "auto",
    },
    # Conditional styling
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#fcfcfc",
        },
        {
            "if": {"state": "selected"},
            "backgroundColor": "#e6f3ff",
            "border": "1px solid #0d6efd",
        },
        {
            "if": {"state": "active"},
            "backgroundColor": "#e6f3ff",
            "border": "1px solid #0d6efd",
        },
    ],
    # Filter styling
    style_filter={
        "backgroundColor": "#f8f9fa",
        "padding": "8px 15px",
    },
    # Additional features
    tooltip_delay=0,
    tooltip_duration=None,
    # Make it more interactive
    editable=False,
    row_selectable=False,
    row_deletable=False,
    # CSS classes for further styling if needed
    css=[
        {
            "selector": ".dash-table-tooltip",
            "rule": "background-color: white; font-family: system-ui; padding: 8px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);",
        }
    ],
)
table_container = html.Div([table], className="p-4 bg-white rounded shadow-sm")

# Programa Bolsa Família
pbf = all_data["pbf_munic_selecionados"].copy()


def get_pbf_plots(pbf):

    # GRÁFICO NÚMERO DE FAVORECIDOS
    fig_n_favorecidos = px.line(
        pbf,
        x="mes_referencia",
        y="n_favorecidos",
        color="nome_municipio",
        line_shape="spline",
        labels={
            "mes_referencia": "Mês",
            "n_favorecidos": "Contagem de famílias beneficiadas",
            "nome_municipio": "Município",
        },
        template="none",
    )
    fig_n_favorecidos.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco (SP)" else 1.5,
                dash="solid" if trace.name == "Osasco (SP)" else "dot",
            ),
            opacity=1 if trace.name == "Osasco (SP)" else 0.7,
        )
    )
    fig_n_favorecidos.update_xaxes(tickformat="%m/%Y")
    fig_n_favorecidos.update_yaxes(tickformat=",")
    fig_n_favorecidos.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(gridcolor="lightgray", zeroline=False, title_standoff=30),
        xaxis=dict(gridcolor="white", zeroline=False, title_standoff=30),
        legend_title_text="Município",
        legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="center", x=0.5),
        margin=dict(b=120),
    )
    fig_n_favorecidos.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Mês/Ano: %{x}<br>Número de favorecidos PBF: %{y:,.0f}<extra></extra>"
    )

    # GRÁFICO TOTAL DE REPASSES
    fig_total_repasses = px.line(
        pbf,
        x="mes_referencia",
        y="total_repasses",
        color="nome_municipio",
        line_shape="spline",
        labels={
            "mes_referencia": "Mês",
            "total_repasses": "Valor total de repasses PBF em reais",
            "nome_municipio": "Município",
        },
        template="none",
    )
    fig_total_repasses.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco (SP)" else 1.5,
                dash="solid" if trace.name == "Osasco (SP)" else "dot",
            ),
            opacity=1 if trace.name == "Osasco (SP)" else 0.7,
        )
    )
    fig_total_repasses.update_xaxes(tickformat="%m/%Y")
    fig_total_repasses.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(gridcolor="lightgray", zeroline=False, title_standoff=30),
        xaxis=dict(gridcolor="white", zeroline=False, title_standoff=30),
        legend_title_text="Município",
        legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="center", x=0.5),
        margin=dict(b=120),
    )
    fig_total_repasses.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Mês/Ano: %{x}<br>Valor total de repasses PBF: %{y:,.0f}<extra></extra>"
    )

    # GRÁFICO MÉDIA DE REPASSES
    fig_media_repasses = px.line(
        pbf,
        x="mes_referencia",
        y="media_repasses",
        color="nome_municipio",
        line_shape="spline",
        labels={
            "mes_referencia": "Mês",
            "media_repasses": "Média do valor dos repasses PBF em reais",
            "nome_municipio": "Município",
        },
        template="none",
    )
    fig_media_repasses.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco (SP)" else 1.5,
                dash="solid" if trace.name == "Osasco (SP)" else "dot",
            ),
            opacity=1 if trace.name == "Osasco (SP)" else 0.7,
        )
    )
    fig_media_repasses.update_xaxes(tickformat="%m/%Y")
    fig_media_repasses.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(gridcolor="lightgray", zeroline=False, title_standoff=30),
        xaxis=dict(gridcolor="white", zeroline=False, title_standoff=30),
        legend_title_text="Município",
        legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="center", x=0.5),
        margin=dict(b=120),
    )
    fig_media_repasses.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Mês/Ano: %{x}<br>Média do valor dos repasses PBF: %{y:,.0f}<extra></extra>"
    )

    for fig in [fig_n_favorecidos, fig_total_repasses, fig_media_repasses]:

        fig.add_annotation(
            text="Fonte: <a href='https://portaldatransparencia.gov.br/download-de-dados/novo-bolsa-familia'>Portal da Transparência: CGU</a>",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.35,
            showarrow=False,
            font=dict(size=12),
            # xanchor="center",
            clicktoshow=False,
        )

    return fig_n_favorecidos, fig_total_repasses, fig_media_repasses


fig_n_favorecidos, fig_total_repasses, fig_media_repasses = get_pbf_plots(pbf)


# DEFINIÇÃO DO VISUAL DA PÁGINA
layout = html.Div(
    [
        html.Br(),
        html.H3("Cadastro Único para Programas Sociais"),
        create_info_popover(
            "info-cadastro-unico",
            "O Cadastro Único proporciona uma visão abrangente da parcela mais vulnerável da população brasileira, permitindo que os governos em todos os níveis saibam quem são essas famílias, onde vivem, suas condições de vida e suas necessidades.",
        ),
        html.Br(),
        # LINHA CARDS COM INFORMAÇÕES GERAIS
        html.Div(
            [
                html.H4("Famílias"),
                html.Br(),
                cards_cadastro,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # INFORMAÇÕES GERAIS - DOMICILIOS
        html.Div(
            [
                html.H4("Domicílios"),
                html.Br(),
                cards_domicilio,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # GRÁFICO DE ALFABETIZADOS E DISTRIBUIÇÃO POR SEXO DOS CADASTROS
        html.Div(
            [row_graficos_cadastro_sexo],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # GRÁFICO DE PARENTESCO DAS PESSOAS CADASTRADAS
        html.Div(
            [
                html.H4("Pessoas cadastradas por parentesco"),
                dcc.Graph(figure=fig_parentesco),
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # TABELA COM VISÃO GERAL DOS BAIRROS DE OSASCO
        html.Div(
            [
                html.H4("Visão geral dos bairros de Osasco"),
                table_container,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        html.Div(
            [
                html.H3("Programa Bolsa Família"),
                html.Br(),
                html.Div(
                    [
                        html.H4(
                            "Número de famílias beneficiadas pelo Programa Bolsa Família"
                        ),
                        dcc.Graph(figure=fig_n_favorecidos),
                    ],
                    className="section-container",
                    style={"marginBottom": "3rem"},
                ),
                html.Div(
                    [
                        html.H4("Valor total dos repasses do Programa Bolsa Família"),
                        dcc.Graph(figure=fig_total_repasses),
                    ],
                    className="section-container",
                    style={"marginBottom": "3rem"},
                ),
                html.Div(
                    [
                        html.H4(
                            "Média do valor dos repasses do Programa Bolsa Família"
                        ),
                        dcc.Graph(figure=fig_media_repasses),
                    ],
                    className="section-container",
                    style={"marginBottom": "3rem"},
                ),
            ]
        ),
    ]
)
