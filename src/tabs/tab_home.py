from dash import html

tab_home = html.Div(
    [
        html.Br(),
        html.H4(
            "Bem-vindo ao Painel de Governo da Prefeitura de Osasco",
            style={"color": "#213953", "fontSize": "20px", "fontWeight": "bold"},
        ),
        html.P("Navegue entre as abas disponíveis:"),
        html.Ul(
            [
                html.Li(
                    "Desenvolvimento Econômico: dados do PIB municipal disponibilizados pelo IBGE;"
                ),
                html.Li("Trabalho e Renda: dados do CAGED e RAIS Estabelecimentos;"),
                html.Li("Desenvolvimento Urbano: visualizações integradas ao OzMundi."),
            ]
        ),
        html.Br(),
        html.Hr(),
        html.H6("Painel desenvolvido pela SETIDE em parceria com a InMov."),
    ],
    className="container",
)
