from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path='/', name='Painel de Governo PMO')

nav_buttons = dbc.Row([
    dbc.Col(
        dbc.CardLink(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Span("trending_up", className="material-icons me-3", style={"fontSize": "1.5rem"}),  # Changed this line
                        html.Span("Desenvolvimento Econômico", style={"fontSize": "0.8rem"})
                    ], style={
                        "display": "flex",
                        "alignItems": "center",
                        "color": "#213953",
                        "textDecoration": "none",
                        "minHeight": "50px",
                        "width": "100%"
                    }),
                ]),
                style={
                    "backgroundColor": "white",
                    "borderRadius": "10px",
                    "boxShadow": "0px 4px 12px rgba(0, 0, 0, 0.1)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                },
                className="mb-3 hover-card"
            ),
            href="/desenvolvimento_economico",
            style={"textDecoration": "none"},
        ),
        width=4,
    ),
    dbc.Col(
        dbc.CardLink(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Span("work", className="material-icons me-3"),  # Changed this line
                        html.Span("Trabalho e Renda", style={"fontSize": "0.8rem"})
                    ], style={
                        "display": "flex",
                        "alignItems": "center",
                        "color": "#213953",
                        "textDecoration": "none",
                        "minHeight": "50px",
                        "width": "100%"
                    }),
                ]),
                style={
                    "backgroundColor": "white",
                    "borderRadius": "10px",
                    "boxShadow": "0px 4px 12px rgba(0, 0, 0, 0.1)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                },
                className="mb-3 hover-card"
            ),
            href="/trabalho_renda",
            style={"textDecoration": "none"},
        ),
        width=4,
    ),
    dbc.Col(
        dbc.CardLink(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Span("location_city", className="material-icons me-3"),  # Changed this line
                        html.Span("Desenvolvimento Urbano", style={"fontSize": "0.8rem"})
                    ], style={
                        "display": "inline-flex",
                        "alignItems": "center",
                        "color": "#213953",
                        "textDecoration": "none",
                        "minHeight": "50px",
                        "width": "100%"
                    }),
                ]),
                style={
                    "backgroundColor": "white",
                    "borderRadius": "10px",
                    "boxShadow": "0px 4px 12px rgba(0, 0, 0, 0.1)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                },
                className="mb-3 hover-card"
            ),
            href="/desenvolvimento_urbano",
            style={"textDecoration": "none"},
        ),
        width=4,
    ),
], className="mt-3", justify="center")

layout = html.Div(
    [
        html.Br(),
        html.H3(
            "Bem-vindo ao Painel de Governo da Prefeitura de Osasco",
            style={"color": "#213953", "fontWeight": "bold"},
            className="text-center mb-4"
        ),
        dbc.Container([
            html.P(
                "Navegue pelas páginas abaixo:",
                className="text-center",
                style={"color": "#213953", "fontSize": "16px"}
            ),
        ]),
        dbc.Container(
            nav_buttons,
            style={"maxWidth": "600px"}
        ),
        
        dbc.Container([
            html.Ul([
                html.Li(
                    [
                        html.Strong("Desenvolvimento Econômico: "),
                        "Indicadores relacionados ao PIB municipal, participação no PIB estadual e PIB per capita."
                    ],
                    style={"marginBottom": "10px"}
                ),
                html.Li(
                    [
                        html.Strong("Trabalho e Renda: "),
                        "Dados sobre empregos formais, movimentações do CAGED, salários e perfil etário dos trabalhadores."
                    ],
                    style={"marginBottom": "10px"}
                ),
                html.Li(
                    [
                        html.Strong("Desenvolvimento Urbano: "),
                        "Informações sobre o zoneamento municipal e uso do solo."
                    ],
                    style={"marginBottom": "10px"}
                ),
            ], style={
                "listStyleType": "none",
                "padding": "20px",
                "maxWidth": "800px",
                "margin": "0 auto",
                "color": "#213953",
                "fontSize": "16px"
            }),
        ]),

        html.Hr(),
        html.H6("Painel desenvolvido pela SETIDE em parceria com a InMov.",
                className="text-center"),
    ],
    className="container",
)