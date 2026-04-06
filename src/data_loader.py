import pandas as pd
import logging #logging para manejo de logs
from pathlib import Path # path sirve para manejar rutas de archivos de manera más eficiente

logger = logging.getLogger(__name__) 

def cargar_base(config):
    """Carga la base de datos desde archivo Excel con validación."""
    try:
        columnas_str = ['Subpartida', '2 digitos', 'CADU', 'RUC', 'CVIATRA', '4 digitos']
        
        file = config.DATA_RAW / f"BD_Expo_{config.ANIOS[0]-1}-{config.ANIOS[0]}_{config.MES_ACTUAL}.xlsx"
        
        if not file.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file}")
        
        logger.info(f"Cargando archivo: {file}")
        df = pd.read_excel(
            file,
            keep_default_na=False, # Evita convertir celdas vacías a NaN
            dtype={col: 'str' for col in columnas_str}
        )
        
        logger.info(f"Base cargada con éxito: {len(df)} registros")
        return df
    except FileNotFoundError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.error(f"Error al cargar base: {str(e)}")
        raise


def cargar_correlaciones(config):
    """Carga archivos de correlaciones con validación."""
    try:
        logger.info("Cargando correlaciones...")
        
        archivo_pais = config.DATA_RAW / "correlac_2022_pais.dta"
        archivo_prod = config.DATA_RAW / "correlac_2022_prod.xlsx"
        archivo_cap = config.DATA_RAW / "correlac_2022_capitulo.dta"
        
        for archivo in [archivo_pais, archivo_prod, archivo_cap]:
            if not archivo.exists():
                raise FileNotFoundError(f"Archivo faltante: {archivo}")
        
        correlac_pais = pd.read_stata(archivo_pais)
        correlac_prod = pd.read_excel(archivo_prod)
        correlac_cap = pd.read_stata(archivo_cap)
        
        logger.info(f"Correlaciones cargadas exitosamente")
        return correlac_pais, correlac_prod, correlac_cap
    except Exception as e:
        logger.error(f"Error cargando correlaciones: {str(e)}")
        raise