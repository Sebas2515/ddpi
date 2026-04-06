"""Configuración centralizada del proyecto.

Define rutas de entrada/salida, parámetros temporales y funciones de período.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 📥 Inputs
DATA_RAW = BASE_DIR / "data" / "raw"
TEMPLATES = BASE_DIR / "templates"

# 📤 Outputs
OUTPUTS = BASE_DIR / "outputs"
OUTPUT_TABLAS = OUTPUTS / "tablas"
OUTPUT_REPORTES = OUTPUTS / "reportes"

# ⚙️ Parámetros
ANIOS = [2026, 2025] # Años a procesar (ANIOS[0] = año actual, ANIOS[1] = año anterior)
MES_NUM = [2, 3] # Meses a procesar (1=Enero, 2=Febrero, etc.)
MES_ACTUAL = "feb" # Cambiar según el mes actual (ene, feb, mar, etc.)
 
def construir_periodos():
    """Construye dinámicamente los periodos según el mes actual.
    
    Returns:
        tuple: (periodo_crear, periodos) donde periodo_crear es lista de 3 periodos
               y periodos es lista con año anterior + 3 periodos creados.
    """
    if MES_ACTUAL == "feb":
        periodo_crear = [
            f"Ene {str(ANIOS[0]-1)[-2:]}",
            f"Ene {str(ANIOS[0])[-2:]}",
            "Ult_12_meses"
        ]
    else:
        periodo_crear = [
            f"Ene-{MES_ACTUAL} {str(ANIOS[0]-1)[-2:]}",
            f"Ene-{MES_ACTUAL} {str(ANIOS[0])[-2:]}",
            "Ult_12_meses"
        ]

    periodos = [str(ANIOS[1]), periodo_crear[0], periodo_crear[1], periodo_crear[2]]
    return periodo_crear, periodos



# # Ahora accedes a:
# periodo_crear[0]   = "Ene-feb 25"
# periodo_crear[1]   = "Ene-feb 26"
# periodo_crear[2]   = "Ult_12_meses"

# periodos = ["2025", "Ene-feb 25", "Ene-feb 26", "Ult_12_meses"]
