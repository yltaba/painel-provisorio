import locale
from pathlib import Path

# FORMATAÇÃO DOS VALORES BR
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

# TEMPLATE DO DASHBOARD
TEMPLATE = "simple_white"

# CAMINHO DOS DADOS
DATA_PATH = Path().resolve() / "data"