import logging

import pandas as pd

logger = logging.getLogger(__name__)


def generar_indices(df, sectores, periodos, periodo_orden):
    """Genera diccionario de indices para todos los sectores."""
    try:
        logger.info("Generando indices por sector...")

        indices = {
            'indice_agro': _generar_indice_sector(df, 'Agropecuario', periodos, periodo_orden),
            'indice_pesca': _generar_indice_sector(df, 'Pesquero', periodos, periodo_orden),
            'indice_textil': _generar_indices_textil(df, periodos, periodo_orden),
        }

        logger.info("Indices generados exitosamente")
        return indices
    except Exception as e:
        logger.error(f"Error generando indices: {str(e)}")
        raise


def _generar_indice_sector(df, sector, periodos, periodo_orden):
    """Genera indices para un sector especifico."""
    try:
        data_filtrada = df[(df['sector2'] == sector) & (df['periodo'].isin(periodos))]
        indice_dict = _generar_indice_desde_df(data_filtrada, periodos, periodo_orden)

        logger.debug(f"Indices del sector {sector} generados")
        return indice_dict
    except Exception as e:
        logger.error(f"Error generando indice para {sector}: {str(e)}")
        raise


def _generar_indices_textil(df, periodos, periodo_orden):
    """Genera todos los bloques requeridos por la hoja Indices_X_Textil."""
    try:
        data_textil = df[(df['sector2'] == 'Textil') & (df['periodo'].isin(periodos))]

        definiciones = {
            'total': pd.Series(True, index=data_textil.index),
            'confecciones': data_textil['grupo2'] == 'Confecciones',
            'prendas_vestir': (
                (data_textil['grupo2'] == 'Confecciones') &
                (data_textil['producto2'] == 'Prendas de vestir')
            ),
            'otras_confecciones': (
                (data_textil['grupo2'] == 'Confecciones') &
                (data_textil['producto2'] == 'Otras confecciones')
            ),
            'textiles': data_textil['grupo2'] == 'Textiles',
            'fibras_textiles': (
                (data_textil['grupo2'] == 'Textiles') &
                (data_textil['producto2'] == 'Fibras textiles')
            ),
            'tejidos': (
                (data_textil['grupo2'] == 'Textiles') &
                (data_textil['producto2'] == 'Tejidos')
            ),
            'hilos_hilados': (
                (data_textil['grupo2'] == 'Textiles') &
                (data_textil['producto2'] == 'Hilos e Hilados')
            ),
        }

        indices_textil = {}
        for etiqueta, filtro in definiciones.items():
            indices_textil[etiqueta] = _generar_indice_desde_df(
                data_textil[filtro],
                periodos,
                periodo_orden,
            )

        logger.debug("Indices de Textil generados")
        return indices_textil
    except Exception as e:
        logger.error(f"Error generando indices de Textil: {str(e)}")
        raise


def _generar_indice_desde_df(data_filtrada, periodos, periodo_orden):
    """Genera tablas de TM y FOB para un subconjunto filtrado."""
    indice_dict = {}

    if data_filtrada.empty:
        indice_dict['TM_sector'] = pd.DataFrame(columns=periodos)
        indice_dict['FOB_sector'] = pd.DataFrame(columns=periodos)
        return indice_dict

    tabla_tm = data_filtrada.pivot_table(
        index='codigo_partida',
        columns='periodo',
        values='miles_TM',
        aggfunc='sum',
    ).sort_values(by=periodo_orden, ascending=False)
    indice_dict['TM_sector'] = tabla_tm

    tabla_fob = data_filtrada.pivot_table(
        index='codigo_partida',
        columns='periodo',
        values='millones_fob',
        aggfunc='sum',
    ).sort_values(by=periodo_orden, ascending=False)
    indice_dict['FOB_sector'] = tabla_fob

    return indice_dict
