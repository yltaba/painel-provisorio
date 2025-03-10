import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        html.Br(),
        html.H3("Este é o Painel de Governo da Prefeitura de Osasco"),
        html.H2("Selecione uma categoria para visualizar os dados"),
    ]
)
