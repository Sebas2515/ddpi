import logging

import pandas as pd

logger = logging.getLogger(__name__)


def cargar_base(config):
    """Mantiene compatibilidad cargando solo la base de exportaciones."""
    return cargar_base_exportaciones(config)


def cargar_bases(config):
    """Carga y normaliza las bases de exportaciones e importaciones."""
    try:
        return {
            'exportaciones': cargar_base_exportaciones(config),
            'importaciones': cargar_base_importaciones(config),
        }
    except Exception as e:
        logger.error(f"Error cargando bases: {str(e)}")
        raise


def cargar_base_exportaciones(config):
    """Carga la base mensual de exportaciones."""
    try:
        columnas_str = ['Subpartida', '2 digitos', 'CADU', 'RUC', 'CVIATRA', '4 digitos']
        archivo = _buscar_archivo(
            config.DATA_RAW,
            f"BD_Expo_*{config.ANIOS[0]-1}-{config.ANIOS[0]}_{config.MES_ACTUAL}.xlsx",
        )

        logger.info(f"Cargando archivo de exportaciones: {archivo}")
        df = pd.read_excel(
            archivo,
            keep_default_na=False,
            dtype={col: 'str' for col in columnas_str},
        )

        logger.info(f"Base de exportaciones cargada con exito: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"Error al cargar exportaciones: {str(e)}")
        raise


def cargar_base_importaciones(config):
    """Carga y normaliza la base mensual de importaciones."""
    try:
        archivo = _buscar_archivo(
            config.DATA_RAW,
            f"BD_Impo*{config.ANIOS[0]-1}-{config.ANIOS[0]}_{config.MES_ACTUAL}.xlsx",
        )

        logger.info(f"Cargando archivo de importaciones: {archivo}")
        df = pd.read_excel(
            archivo,
            sheet_name='Mensual',
            keep_default_na=False,
            dtype={
                'codigo_partida': 'str',
                'codigo_pais': 'str',
                'codigo_via': 'str',
            },
        )

        df = df.rename(columns={
            'codigo_partida': 'Subpartida',
            'codigo_pais': 'CPAIDES',
            'año': 'AÑO',
            'mes': 'MES',
            'peso_neto': 'VPESNET',
            'fob': 'FOB',
            'flujo_comercial': 'Flujo',
        }).copy()

        df['Subpartida'] = df['Subpartida'].astype(str)
        df['CPAIDES'] = df['CPAIDES'].astype(str)
        df['CADU'] = ''
        df['RUC'] = ''

        logger.info(f"Base de importaciones cargada con exito: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"Error al cargar importaciones: {str(e)}")
        raise


def _buscar_archivo(base_dir, pattern):
    archivos = sorted(base_dir.glob(pattern))
    if not archivos:
        raise FileNotFoundError(f"No se encontro archivo con patron: {pattern}")
    return archivos[0]


def cargar_correlaciones(config):
    """Carga archivos de correlaciones con validacion."""
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

        logger.info("Correlaciones cargadas exitosamente")
        return correlac_pais, correlac_prod, correlac_cap
    except Exception as e:
        logger.error(f"Error cargando correlaciones: {str(e)}")
        raise
