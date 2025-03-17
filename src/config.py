# import locale
# from pathlib import Path

# # FORMATAÇÃO DOS VALORES BR
# locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

# # TEMPLATE DO DASHBOARD
# TEMPLATE = "simple_white"

# # CAMINHO DOS DADOS
# DATA_PATH = Path().resolve() / "data"


from pathlib import Path

# Add a function to format numbers consistently
def format_number(value, currency=False, decimals=2):
    """Format numbers consistently regardless of locale."""
    try:
        if currency:
            return f"R$ {value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(value)

TEMPLATE = "simple_white"

# File paths
DATA_PATH = Path().resolve() / "data"