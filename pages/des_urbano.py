from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path='/desenvolvimento_urbano', name='Desenvolvimento Urbano')

layout = html.Div(
    [
    dbc.Row(
            dbc.Col(
                dbc.Button(
                    [
                        html.Span("home", className="material-icons me-2", 
                            style={"display": "inline-flex", "verticalAlign": "middle"}),
                        html.Span("Voltar para Home", 
                            style={"verticalAlign": "middle"})
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
                        "gap": "4px",
                        "textTransform": "none"
                    }
                ),
                className="d-flex justify-content-end"  # This aligns the content to the right
            )
        ),
        html.Br(),
        html.H4("Zoneamento de Osasco"),
        html.Iframe(
            src="https://ozmundi.osasco.sp.gov.br/misc/base_zoneamento/",
            style={
                "width": "100%",
                "height": "1000px",
                "border": "none",
            },
        ),
    ]
)