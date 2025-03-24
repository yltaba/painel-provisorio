from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash

from src.config import DATA_PATH
from src.load_data import load_data
from src.callbacks import init_callbacks


external_stylesheets = [
    dbc.themes.SANDSTONE,
    "https://fonts.googleapis.com/icon?family=Material+Icons", 
]
app = Dash(
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
app.title = "Painel de Governo PMO"

# DADOS
data_path = DATA_PATH
all_data = load_data()


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

navbar = dbc.Nav(
    [
        dbc.NavLink(
            [html.Div(page["name"])],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    pills=True,
    className="mb-3",
)


app.layout = dbc.Container(
    [
        imagem_cabecalho,
        html.Br(),
        dash.page_container,
    ]
)


init_callbacks(app, all_data)

server = app.server
if __name__ == "__main__":
    app.run_server(debug=True)