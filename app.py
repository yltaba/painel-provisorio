from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash

from src.utils import create_breadcrumb
from src.config import DATA_PATH
from src.load_data import load_data
from src.callbacks import init_callbacks
from src.titulos_index import TITULOS

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
                                "height": "60px",
                                "display": "flex",
                                "alignItems": "center",
                                "padding": "0",
                                "justifyContent": "flex-start",
                                "width": "100%",
                                "marginLeft": "75px",
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
        html.Div(style={"height": "205px"}),
        # Conteúdo da página
        html.Div(
            dash.page_container,
            style={
                "maxWidth": "1400px",
                "margin": "0 auto",
                "width": "100%",
                "padding": "0 20px",
            }
        ),
    ],
    fluid=True,
    style={
        "overflow-x": "hidden",
        "padding-top": "0",
    }
)

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


@app.callback(
    Output('resultados-busca', 'children'),
    Input('input-busca', 'value')
)
def buscar_titulos(termo):
    if not termo:
        return ""
    resultados = [t for t in TITULOS if termo.lower() in t["titulo"].lower()]
    if not resultados:
        return html.Div("Nenhum resultado encontrado.", style={"padding": "8px", "color": "#888"})
    return html.Ul(
        [
            html.Li(
                html.A(
                    [
                        html.I(className="material-icons", children="search", style={"fontSize": "18px", "verticalAlign": "middle", "marginRight": "8px"}),
                        t["titulo"],
                        # html.Span(f" ({t['pagina']})", style={"color": "#888", "fontSize": "13px", "marginLeft": "8px"})
                    ],
                    href=f"/{t['pagina']}#{t['ancora']}",
                    style={"textDecoration": "none", "color": "#0B3B7F"}
                ),
                style={
                    "padding": "6px 12px",
                    "borderBottom": "1px solid #eee",
                    "listStyle": "none",
                    "cursor": "pointer"
                }
            )
            for t in resultados
        ],
        style={
            "background": "#fff",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
            "borderRadius": "6px",
            "margin": "8px 0 0 0",
            "padding": "0",
            "maxHeight": "260px",
            "overflowY": "auto",
            "minWidth": "320px",
            "position": "absolute",
            "zIndex": 2000
        }
    )


# Callback de conteúdo da página
@app.callback(Output("page-content", "children"), [Input("authenticated", "data")])
def display_page(authenticated):
    if not authenticated:
        return login_layout
    return main_layout


@app.callback(
    Output("back-button-container", "children"),
    Input("url", "pathname")
)
def toggle_navigation(pathname):
    if pathname == "/" or pathname == "":
        return html.Div(
            [
                dcc.Input(
                    id='input-busca',
                    type='text',
                    placeholder='Buscar gráfico ou indicador...',
                    style={
                        "width": "320px",
                        "height": "32px",  # Próximo da altura da barra azul
                        "fontSize": "16px",
                        "borderRadius": "6px",
                        "padding": "0 12px",
                        "border": "1px solid #ccc",
                        "boxSizing": "border-box",
                        "margin": "0"
                    }
                ),
                html.Div(id='resultados-busca')
            ],
            style={
                "position":"relative",
                "width":"320px",
            }
        )
    elif pathname and pathname != "/login":
        return html.Div(
            create_breadcrumb(pathname),
            style={
                "display": "flex",
                "alignItems": "center",
                "height": "100%",
                "paddingLeft": "24px"
            }
        )
    return None

init_callbacks(app, all_data)

server = app.server
if __name__ == "__main__":
    app.run_server(debug=True) 