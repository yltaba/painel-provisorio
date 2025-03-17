from dash import html


tab_desenvolvimento_urbano = html.Div(
    [
        html.Br(),
        html.H4("Zoneamento de Osasco"),
        html.Iframe(
            src="https://ozmundi.osasco.sp.gov.br/misc/base_zoneamento/",
            style={
                "width": "100%",
                "height": "500px",
                "border": "none",
            },
        ),
    ]
)