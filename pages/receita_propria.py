from dash import dcc, html, register_page, dash_table  # Add dash_table import
import dash_bootstrap_components as dbc
import plotly.express as px
from babel.numbers import format_decimal, format_currency

from src.utils import (
    calcular_pib_atual,
    calcular_variacao_pib,
    create_info_popover,
    get_options_dropdown,
)
from src.config import TEMPLATE
from src.load_data import load_data


register_page(
    __name__, path="/gestao_receita_propria", name="Gestão da Receita Própria"
)

# CARREGAR DADOS
all_data = load_data()

layout = html.Div(
    [
        html.P("teste")
    ]
)
