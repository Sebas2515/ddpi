"""
Módulo de procesamiento RMC (Reporte Mensual de Comercio).
Automatiza la carga, procesamiento y exportación de datos comerciales.
"""

from src.pipeline import run_pipeline
from src.config import construir_periodos

__all__ = [
    'run_pipeline',
    'construir_periodos',
]

__version__ = '1.0.0'
__author__ = 'DDPI'
__description__ = 'Pipeline de automatización RMC - Procesamiento de datos de comercio exterior'
