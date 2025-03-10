import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H1("Dashboard Layout Example", className="text-center mb-4"), #mb-4 adiciona margem abaixo do texto.
        dbc.Row(
            [
                dbc.Col(html.Div("Column 1"), width=6),
                dbc.Col(html.Div("Column 2"), width=6),
            ],
            justify="center",
            align="center"
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("Column A"), width=6),
                dbc.Col(html.Div("Column B"), width=6),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
