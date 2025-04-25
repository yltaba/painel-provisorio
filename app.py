from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash

from src.utils import create_breadcrumb
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
    # debug=False,
)
app.title = "Painel de Governo PMO"

# DADOS
data_path = DATA_PATH
all_data = load_data()


imagem_cabecalho = html.Img(
    src="/assets/Marca-Osasco-Digital-COLOR-ALTA-02.svg",
    style={
        "width": "350px",
        "height": "auto",
        "display": "block",
        "margin": "10px 20px",  # Remove a margem lateral, mantém só topo e base
        "padding-left": "0",  # Garante que não há padding à esquerda
    },
)

# Login layout
login_layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Login Painel de Governo PMO", className="text-center"),
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
                        ]
                    ),
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
        # Container fixo para o cabeçalho
        html.Div(
            [
                # Barra azul fina superior
                html.Div(
                    style={
                        "backgroundColor": "#0B3B7F",
                        "width": "100%",
                        "height": "35px",
                        "marginLeft": "-24px",
                        "marginRight": "-24px",
                        "width": "calc(100% + 48px)",
                    }
                ),
                html.Div(
                    [
                        imagem_cabecalho,
                    ],
                    style={
                        "maxWidth": "1400px",  # Add max-width
                        "margin": "0 auto",    # Center the content
                        "width": "100%",
                    }
                ),
                # Barra azul marinho com botão voltar condicional
                html.Div(
                    [
                        dbc.Container(
                            id="back-button-container",
                            fluid=True,
                            style={
                                "height": "75px",
                                "display": "flex",
                                "alignItems": "center",
                                "padding": "0",
                                "justifyContent": "flex-end",
                                "width": "100%",
                            }
                        )
                    ],
                    style={
                        "backgroundColor": "#0B3B7F",
                        "height": "60px",
                        "marginLeft": "-24px",
                        "marginRight": "-24px",
                        "width": "calc(100% + 48px)",
                    }
                ),
            ],
            style={
                "position": "fixed",  # Fixa o cabeçalho
                "top": 0,  # Alinha ao topo
                "left": 0,  # Alinha à esquerda
                "right": 0,  # Alinha à direita
                "backgroundColor": "white",  # Fundo branco para o cabeçalho
                "zIndex": 1000,  # Garante que fique acima de outros elementos
                "width": "100%",
                "paddingLeft": "24px",  # Adiciona padding para alinhar com o container
                "paddingRight": "24px",
            }
        ),
        # Div para criar espaço para o conteúdo não ficar embaixo do cabeçalho fixo
        html.Div(style={"height": "205px"}),  # Ajuste este valor conforme a altura total do seu cabeçalho
        # Conteúdo da página
        html.Div(
            dash.page_container,
            style={
                "maxWidth": "1400px",  # Match header max-width
                "margin": "0 auto",    # Center the content
                "width": "100%",
                "padding": "0 20px",   # Add some padding on the sides
            }
        ),
    ],
    fluid=True,
    style={
        "overflow-x": "hidden",
        "padding-top": "0",  # Remove o padding top do container principal
    }
)

# Callback para controlar a visibilidade do breadcrumb
@app.callback(
    Output("back-button-container", "children"),
    Input("url", "pathname")
)
def toggle_navigation(pathname):
    if pathname == "/" or pathname == "":  # Se estiver na página inicial
        return None  # Não mostra o breadcrumb
    return create_breadcrumb(pathname)  # Mostra o breadcrumb em todas as outras páginas



# Layout + autenticação
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="authenticated", storage_type="session"),
        html.Div(id="page-content"),
    ]
)


# Callback de autenticação
@app.callback(
    [Output("authenticated", "data"), Output("login-error", "children")],
    [Input("login-button", "n_clicks")],
    [State("password", "value")],
    prevent_initial_call=True,
)
def authenticate(n_clicks, password):
    if not n_clicks:
        return False, ""
    if password == VALID_PASSWORD:
        return True, ""
    return False, "Senha incorreta"


# Callback de conteúdo da página
@app.callback(Output("page-content", "children"), [Input("authenticated", "data")])
def display_page(authenticated):
    if not authenticated:
        return login_layout
    return main_layout


init_callbacks(app, all_data)

server = app.server
if __name__ == "__main__":
    app.run_server(debug=False)
