from dash import html
import dash_bootstrap_components as dbc
from babel.numbers import format_currency, format_percent, format_compact_currency


def get_options_dropdown(all_data, table, column):
    sorted_values = sorted(all_data[table][column].dropna().unique())
    return [{"label": x, "value": x} for x in sorted_values]


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
    pib_corrente = format_compact_currency(pib_corrente_int, 'BRL', locale='pt_BR', fraction_digits=2)
    return pib_corrente


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

    variacao_pib = ((pib_ano - pib_ano_anterior) / pib_ano_anterior)
    variacao_pib = format_percent(variacao_pib, format='#,##0.0%', locale='pt_BR')

    return variacao_pib


def create_info_popover(id_referencia, texto):
    return html.Div(
        [
            dbc.Button(
                html.I(className="material-icons", children="info"),
                id=id_referencia,
                color="link",
                size="sm",
                className="p-0 ms-2",
                style={"color": "#213953"},
            ),
            dbc.Popover(
                dbc.PopoverBody(texto),
                target=id_referencia,
                trigger="hover",
                placement="right",
            ),
        ],
        style={"display": "inline-block"},
    )


def botao_voltar():
    return html.Div(
        [
            dbc.Row(
                dbc.Col(
                dbc.Button(
                    [
                        html.Span(
                            "home",
                            className="material-icons",  # Removido me-2 pois não precisamos de margem
                            style={
                                "display": "flex",  # Mudado para flex
                                "alignItems": "center",  # Centraliza verticalmente
                                "justifyContent": "center",  # Centraliza horizontalmente
                                "height": "100%",  # Garante que ocupa toda altura do botão
                            },
                        ),
                    ],
                    href="/",
                    color="light",
                    className="mb-3",
                    style={
                        "textDecoration": "none",
                        "display": "flex",  # Mudado para flex
                        "alignItems": "center",  # Centraliza verticalmente
                        "justifyContent": "center",  # Centraliza horizontalmente
                        "width": "50px",  # Largura fixa para o botão ser quadrado
                        "height": "35px",  # Altura fixa para o botão ser quadrado
                        "padding": "0",  # Remove padding interno
                    },
                ),
                className="d-flex justify-content-end",
            )
        ),
    ],
    className="section-container",
    style={"marginBottom": "1rem"},
)