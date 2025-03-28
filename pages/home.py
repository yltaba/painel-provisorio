from dash import html, register_page
import dash_bootstrap_components as dbc
from src.config import footer

register_page(__name__, path="/", name="Painel de Governo PMO")

# BOTÕES DE NAVEGAÇÃO
nav_buttons = dbc.Row(
    [
        dbc.Col(
            dbc.CardLink(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        "trending_up",
                                        className="material-icons me-3",
                                        style={"fontSize": "2rem", "color": "#99d98c"},
                                    ),  
                                    html.Span(
                                        "Desenvolvimento Econômico",
                                        style={
                                            "fontSize": "1rem",
                                            "textAlign": "center",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "color": "#213953",
                                    "textDecoration": "none",
                                    "minHeight": "50px",
                                    "width": "100%",
                                },
                            ),
                        ]
                    ),
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxShadow": "0px 4px 12px rgba(0, 0, 0, 0.1)",
                        "transition": "transform 0.2s ease-in-out",
                        "cursor": "pointer",
                    },
                    className="mb-3 hover-card",
                ),
                href="/desenvolvimento_economico",
                style={"textDecoration": "none"},
            ),
            width=4,
        ),
        dbc.Col(
            dbc.CardLink(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        "work",
                                        className="material-icons me-3",
                                        style={"fontSize": "2rem", "color": "#34a0a4"},
                                    ),  
                                    html.Span(
                                        "Trabalho e Renda",
                                        style={
                                            "fontSize": "1rem",
                                            "textAlign": "center",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "color": "#213953",
                                    "textDecoration": "none",
                                    "minHeight": "50px",
                                    "width": "100%",
                                },
                            ),
                        ]
                    ),
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxShadow": "0px 4px 12px rgba(0, 0, 0, 0.1)",
                        "transition": "transform 0.2s ease-in-out",
                        "cursor": "pointer",
                    },
                    className="mb-3 hover-card",
                ),
                href="/trabalho_renda",
                style={"textDecoration": "none"},
            ),
            width=4,
        ),
        dbc.Col(
            dbc.CardLink(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        "location_city",
                                        className="material-icons me-3",
                                        style={"fontSize": "2rem", "color": "#168aad"},
                                    ),  
                                    html.Span(
                                        "Desenvolvimento Urbano",
                                        style={
                                            "fontSize": "1rem",
                                            "textAlign": "center",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "inline-flex",
                                    "alignItems": "center",
                                    "color": "#213953",
                                    "textDecoration": "none",
                                    "minHeight": "50px",
                                    "width": "100%",
                                },
                            ),
                        ]
                    ),
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxShadow": "0px 4px 12px rgba(0, 0, 0, 0.1)",
                        "transition": "transform 0.2s ease-in-out",
                        "cursor": "pointer",
                    },
                    className="mb-3 hover-card",
                ),
                href="/desenvolvimento_urbano",
                style={"textDecoration": "none"},
            ),
            width=4,
        ),


        dbc.Col(
            dbc.CardLink(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        "group",
                                        className="material-icons me-3",
                                        style={"fontSize": "2rem", "color": "#1e6091"},
                                    ),  
                                    html.Span(
                                        "Desenvolvimento Humano",
                                        style={
                                            "fontSize": "1rem",
                                            "textAlign": "center",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "inline-flex",
                                    "alignItems": "center",
                                    "color": "#213953",
                                    "textDecoration": "none",
                                    "minHeight": "50px",
                                    "width": "100%",
                                },
                            ),
                        ]
                    ),
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxShadow": "0px 4px 12px rgba(0, 0, 0, 0.1)",
                        "transition": "transform 0.2s ease-in-out",
                        "cursor": "pointer",
                    },
                    className="mb-3 hover-card",
                ),
                href="/desenvolvimento_humano",
                style={"textDecoration": "none"},
            ),
            width=4
        ),


    ],
    className="mt-3",
    justify="center",
)


layout = html.Div(
    [
        html.Div(
            [
                html.H3(
                    "Bem-vindo ao Painel de Governo da Prefeitura de Osasco!",
                    style={"color": "#213953", "fontWeight": "bold"},
                    className="text-center mb-4",
                ),
                dbc.Container(
                    [
                        html.P(
                            "Navegue pelas páginas abaixo:",
                            className="text-center",
                            style={"color": "#213953", "fontSize": "16px"},
                        ),
                    ]
                ),
                dbc.Container(nav_buttons, style={"maxWidth": "750px"}),
            ],
            style={
                "marginTop": "2rem",
                "marginBottom": "2rem",
            },
        ),
        html.Div(
            footer,
            style={
                "position": "fixed",
                "bottom": 0,
                "width": "100%",
                "left": 0,
            }
        ),
    ],
)