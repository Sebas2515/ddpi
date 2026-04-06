import pandas as pd
import logging

logger = logging.getLogger(__name__)

def generar_indices(df, sectores, periodos, periodo_orden):
    """Genera diccionario de índices para todos los sectores."""
    try:
        logger.info("Generando índices por sector...")
        
        indices = {
            'indice_agro': _generar_indice_sector(df, 'Agropecuario', periodos, periodo_orden),
            'indice_pesca': _generar_indice_sector(df, 'Pesquero', periodos, periodo_orden),
            'indice_textil': _generar_indice_sector(df, 'Textil', periodos, periodo_orden)
        }
        
        logger.info("Índices generados exitosamente")
        return indices
    except Exception as e:
        logger.error(f"Error generando índices: {str(e)}")
        raise


def _generar_indice_sector(df, sector, periodos, periodo_orden):
    """Genera índices para un sector específico."""
    try:
        indice_dict = {}
        
        # TM por código de partida
        data_tm = df[(df['sector2']==sector) & (df['periodo'].isin(periodos))]
        tabla_tm = data_tm.pivot_table(
            index='codigo_partida',
            columns='periodo',
            values='miles_TM',
            aggfunc='sum'
        ).sort_values(by=periodo_orden, ascending=False)
        indice_dict['TM_sector'] = tabla_tm
        
        # FOB por código de partida
        tabla_fob = data_tm.pivot_table(
            index='codigo_partida',
            columns='periodo',
            values='millones_fob',
            aggfunc='sum'
        ).sort_values(by=periodo_orden, ascending=False)
        indice_dict['FOB_sector'] = tabla_fob
        
        logger.debug(f"Índices del sector {sector} generados")
        return indice_dict
    except Exception as e:
        logger.error(f"Error generando índice para {sector}: {str(e)}")
        raise
