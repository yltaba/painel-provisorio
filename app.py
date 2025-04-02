from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash

from src.config import DATA_PATH
from src.load_data import load_data
from src.callbacks import init_callbacks

VALID_PASSWORD = "Oz1962"

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
        "width": "40%",
        "height": "40%",
        "display": "block",
        "margin": "auto",
        "margin-top": "15px",
    },
)

# Login layout
login_layout = dbc.Container(
    [
        imagem_cabecalho,
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Login", className="text-center"),
                        html.Br(),
                        dbc.Input(
                            type="password",
                            id="password",
                            placeholder="Digite a senha",
                            className="mb-3",
                        ),
                        dbc.Button(
                            "Entrar",
                            id="login-button",
                            color="primary",
                            className="w-100",
                        ),
                        html.Div(id="login-error", className="text-danger mt-3"),
                    ]),
                ),
                width={"size": 6, "offset": 3},
            ),
        ),
    ],
    className="mt-5",
)

# Main app layout
main_layout = dbc.Container(
    [
        imagem_cabecalho,
        html.Br(),
        dash.page_container,
    ]
)

# Layout + autenticação
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='authenticated', storage_type='session'),
    html.Div(id='page-content')
])

# Callback de autenticação
@app.callback(
    [Output('authenticated', 'data'),
     Output('login-error', 'children')],
    [Input('login-button', 'n_clicks')],
    [State('password', 'value')],
    prevent_initial_call=True
)
def authenticate(n_clicks, password):
    if not n_clicks:
        return False, ''
    if password == VALID_PASSWORD:
        return True, ''
    return False, 'Senha incorreta'

# Callback de conteúdo da página
@app.callback(
    Output('page-content', 'children'),
    [Input('authenticated', 'data')]
)
def display_page(authenticated):
    if not authenticated:
        return login_layout
    return main_layout

init_callbacks(app, all_data)

server = app.server
if __name__ == "__main__":
    app.run_server(debug=True)