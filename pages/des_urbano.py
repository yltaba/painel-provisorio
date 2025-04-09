from dash import html, register_page
import dash_bootstrap_components as dbc
from src.utils import create_info_popover

register_page(__name__, path="/desenvolvimento_urbano", name="Desenvolvimento Urbano")

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
        # LOTEAMENTO DE OSASCO
        html.Div(
            [
                html.H4("Loteamento de Osasco"),
                create_info_popover(
                    "info-zoneamento",
                    "",
                ),
                html.Iframe(
                    src="https://ozmundi.osasco.sp.gov.br/misc/base_loteamento/", # https://ozmundi.osasco.sp.gov.br/misc/base_zoneamento/
                    style={
                        "width": "100%",
                        "height": "1000px",
                        "border": "none",
                    },
                ),
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        )

    ]
)
