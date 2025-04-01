from dash import html, register_page, dcc
import pandas as pd
import dash_bootstrap_components as dbc
from src.utils import create_info_popover
import plotly.express as px

from src.load_data import load_data

register_page(__name__, path="/desenvolvimento_humano", name="Desenvolvimento Humano")

all_data = load_data()

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
            "n_favorecidos": "Contagem de favorecidos no município",
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
    fig_n_favorecidos.update_xaxes(
        # tickvals=pbf["mes_referencia"].unique(),
        tickformat="%m/%Y"
    )
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
            "n_favorecidos": "Contagem de favorecidos no município",
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
    fig_total_repasses.update_xaxes(
        tickformat="%m/%Y"
    )
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
            "n_favorecidos": "Contagem de favorecidos no município",
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
    fig_media_repasses.update_xaxes(
        tickformat="%m/%Y"
    )
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

    return fig_n_favorecidos, fig_total_repasses, fig_media_repasses

fig_n_favorecidos, fig_total_repasses, fig_media_repasses = get_pbf_plots(pbf)

layout = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            [
                                html.Span(
                                    "home",
                                    className="material-icons me-2",
                                    style={
                                        "display": "inline-flex",
                                        "verticalAlign": "middle",
                                    },
                                ),
                                html.Span(
                                    "Voltar para página inicial",
                                    style={"verticalAlign": "middle"},
                                ),
                            ],
                            href="/",
                            color="light",
                            className="mb-3",
                            style={
                                "textDecoration": "none",
                                "color": "#213953",
                                "boxShadow": "0px 4px 12px rgba(0, 0, 0, 0.1)",
                                "display": "inline-flex",
                                "alignItems": "center",
                                "textTransform": "none",
                            },
                        ),
                        className="d-flex justify-content-end",
                    )
                ),
            ],
            className="section-container",
            style={"marginBottom": "1rem"},
        ),
        html.Div(
            [
                html.H4("Número de famílias beneficiadas pelo Programa Bolsa Família"),
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
                html.H4("Média do valor dos repasses do Programa Bolsa Família"),
                dcc.Graph(figure=fig_media_repasses),
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
    ]
)
