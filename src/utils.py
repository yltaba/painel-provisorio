from dash import html
import dash_bootstrap_components as dbc


def get_options_dropdown(all_data, table, column):
    return [{"label": x, "value": x} for x in all_data[table][column].dropna().unique()]


def calcular_pib_atual(pib_por_categoria):
    ano_max = pib_por_categoria["ano"].max()
    pib_corrente_int = (
        pib_por_categoria.loc[
            (pib_por_categoria["ano"] == ano_max)
            & (pib_por_categoria["variavel_dash"] == "Total")
        ]["pib_corrente"]
        .values[0]
        .round()
        .astype(int)
    )
    # pib_corrente = locale.format_string("%.0f", pib_corrente_int, grouping=True)
    return pib_corrente_int


def calcular_variacao_pib(pib_por_categoria):
    pib_ano = (
        pib_por_categoria.loc[
            (pib_por_categoria["ano"] == pib_por_categoria["ano"].max())
            & (pib_por_categoria["variavel_dash"] == "Total")
        ]["pib_deflacionado"]
        .values[0]
        .round()
        .astype(int)
    )

    pib_ano_anterior = (
        pib_por_categoria.loc[
            (pib_por_categoria["ano"] == pib_por_categoria["ano"].max() - 1)
            & (pib_por_categoria["variavel_dash"] == "Total")
        ]["pib_deflacionado"]
        .values[0]
        .round()
        .astype(int)
    )

    variacao_pib = ((pib_ano - pib_ano_anterior) / pib_ano_anterior) * 100
    # variacao_pib = locale.format_string("%.1f%%", variacao_pib, grouping=True)
    return variacao_pib


def create_card_valor(title, value, currency=False):
    # Check if the value is a percentage (ends with %)
    is_percentage = isinstance(value, str) and value.strip().endswith("%")

    if is_percentage:
        # Remove % and convert to float
        numeric_value = float(value.replace("%", "").replace(",", "."))
        # Determine arrow and color based on value
        arrow = "⬆" if numeric_value > 0 else "⬇" if numeric_value < 0 else "➡"
        color = "green" if numeric_value > 0 else "red" if numeric_value < 0 else "gray"

        value_display = html.Div(
            [
                html.Span(
                    arrow,
                    style={
                        "color": color,
                        "margin-right": "8px",
                        "font-size": "24px",
                    },
                ),
                html.Span(value, className="card-value"),
            ],
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "width": "100%",
            },
        )
    else:
        value_display = html.Div(
            [
                (html.Span("R$ ", className="currency-symbol") if currency else None),
                html.Span(value, className="card-value"),
            ],
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "width": "100%",
            },
        )

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(title, className="card-title", style={"text-align": "center"}),
                value_display,
            ]
        ),
        className="custom-card",
    )
