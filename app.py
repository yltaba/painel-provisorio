from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash

from src.utils import botao_voltar
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


imagem_cabecalho = html.Img(
    src="https://osasco.sp.gov.br/wp-content/uploads/2024/12/logo-pmo-2025-2028-horizontal.png",
    style={
        "width": "250px",
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
# main_layout = dbc.Container(
#     [
#         # Barra azul fina superior
#         html.Div(
#             style={
#                 "backgroundColor": "#0B3B7F",
#                 "width": "100%",
#                 "position": "relative",
#                 "left": "0",
#                 "right": "0",
#                 "height": "20px",
#                 "marginLeft": "-24px",  # Compensa o padding do Container
#                 "marginRight": "-24px",
#                 "width": "calc(100% + 48px)",  # Ajusta a largura considerando as margens
#             }
#         ),
#         imagem_cabecalho,
#         # Barra azul marinho com botão voltar condicional
#         html.Div(
#             [
#                 dbc.Container(
#                     id="back-button-container",
#                     fluid=True,
#                     style={
#                         "padding": "8px 20px",
#                     }
#                 )
#             ],
#             style={
#                 "backgroundColor": "#0B3B7F",
#                 "position": "relative",
#                 "left": "0",
#                 "right": "0",
#                 "height": "55px",
#                 "marginLeft": "-24px",  # Compensa o padding do Container
#                 "marginRight": "-24px",
#                 "width": "calc(100% + 48px)",  # Ajusta a largura considerando as margens
#             }
#         ),
#         html.Br(),
#         dash.page_container,
#     ],
#     fluid=True,
#     style={
#         "overflow-x": "hidden"  # Mantém a prevenção de rolagem horizontal
#     }
# )



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
                        "height": "30px",
                    }
                ),
                # Logo
                imagem_cabecalho,
                # Barra azul marinho com botão voltar condicional
                html.Div(
                    [
                        dbc.Container(
                            id="back-button-container",
                            fluid=True,
                            style={
                                "padding": "8px 20px",
                            }
                        )
                    ],
                    style={
                        "backgroundColor": "#0B3B7F",
                        "width": "100%",
                        "height": "50px",
                    }
                ),
            ],
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "right": 0,
                "backgroundColor": "white",
                "zIndex": 1000,
                "width": "100%",
            }
        ),
        # Div para compensar o espaço do cabeçalho fixo
        html.Div(
            style={
                "height": "calc(20px + 50px + 80px)",
                "width": "100%",
            }
        ),
        # Container para o conteúdo principal com margens
        dbc.Container(
            dash.page_container,
            fluid=True,
            style={
                "paddingLeft": "40px",  # Margem lateral esquerda
                "paddingRight": "40px",  # Margem lateral direita
                "maxWidth": "1400px",    # Largura máxima do conteúdo
                "margin": "0 auto",      # Centraliza o conteúdo
            }
        ),
    ],
    fluid=True,
    style={
        "padding": "0",
        "overflow-x": "hidden"
    }
)



# Callback para controlar a visibilidade do botão voltar
@app.callback(
    Output("back-button-container", "children"),
    Input("url", "pathname")
)
def toggle_back_button(pathname):
    if pathname == "/" or pathname == "":  # Se estiver na página inicial
        return None  # Não mostra o botão
    return botao_voltar()  # Mostra o botão em todas as outras páginas


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
    app.run_server(debug=True)
