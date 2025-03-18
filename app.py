from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

from src.config import DATA_PATH
from src.load_data import load_data
from src.callbacks import init_callbacks


# DADOS
data_path = DATA_PATH
all_data = load_data()

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
external_stylesheets = [
    dbc.themes.SANDSTONE
]
app = Dash(
    external_stylesheets=external_stylesheets, suppress_callback_exceptions=True
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

app.layout = dbc.Container(
    [
        imagem_cabecalho,
        html.Br(),
        all_tabs,
        html.Div(id="tabs-content"),
    ]
)
init_callbacks(app, all_data)

server = app.server
if __name__ == "__main__":
    app.run_server(debug=True)
