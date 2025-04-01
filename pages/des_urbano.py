from dash import html, register_page
import dash_bootstrap_components as dbc
from src.utils import create_info_popover

register_page(__name__, path="/desenvolvimento_urbano", name="Desenvolvimento Urbano")
import pyodbc
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# data
server = 'ena6obg6j2cevcppw7dn7yu57a-ft5kzcrrso7exn77ioi727kmza.datawarehouse.fabric.microsoft.com'
database = 'cidade_inteligente'

conn = pyodbc.connect(
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server={server};"
    f"Database={database};"
    "Authentication=ActiveDirectoryInteractive"
)

query = """
SELECT TOP (10) [ano],
            [sigla_uf],
            [id_municipio],
            [quantidade_vinculos_ativos],
            [quantidade_vinculos_clt],
            [quantidade_vinculos_estatutarios],
            [tamanho_estabelecimento],
            [cnae_1]
FROM [cidade_inteligente].[dbo].[rais_estab]
"""

df = pd.read_sql(query, conn)

fig = px.histogram(df, x="quantidade_vinculos_ativos", nbins=20)



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
        # ZONEAMENTO DE OSASCO
        html.Div(
            [
                html.H4("Zoneamento de Osasco"),
                create_info_popover(
                    "info-zoneamento",
                    "O zoneamento de Osasco é um plano de uso do solo que define as áreas destinadas a diferentes atividades econômicas e de ocupação do solo.",
                ),
                html.Iframe(
                    src="https://ozmundi.osasco.sp.gov.br/misc/base_zoneamento_2024/", # https://ozmundi.osasco.sp.gov.br/misc/base_zoneamento/
                    style={
                        "width": "100%",
                        "height": "1000px",
                        "border": "none",
                    },
                ),
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        dcc.Graph(figure=fig),
    ]
)
