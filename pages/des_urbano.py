from dash import html, register_page
import dash_bootstrap_components as dbc
from src.utils import create_info_popover

register_page(__name__, path="/desenvolvimento_urbano", name="Desenvolvimento Urbano")

layout = html.Div(
    [
        html.Br(),
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
