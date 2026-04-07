from openpyxl import load_workbook
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def generar_reporte(tablas, indices, config):
    """Genera el reporte Excel escribiendo todas las tablas y datos en la plantilla."""
    try:
        template = config.TEMPLATES / f"Cuadros de RMC-{config.MES_ACTUAL}-{config.ANIOS[0]}-Joel-act.xlsx"
        output = config.OUTPUT_REPORTES / f"RMC_{config.MES_ACTUAL}_{config.ANIOS[0]}.xlsx"
        
        if not template.exists():
            raise FileNotFoundError(f"Plantilla no encontrada: {template}")
        
        config.OUTPUT_REPORTES.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Cargando plantilla: {template}")
        libro = load_workbook(template)

        # LLENAR HOJA COMERCIO_TEXTIL
        logger.info("Escribiendo datos en hoja Comercio_Textil...")
        tabla_final = tablas['tabla_final']
        tabla_destinos = tablas['tabla_destinos']
        num_destinos = tablas['num_destinos']
        
        _escribir_comercio_textil(libro['Comercio_Textil'], tabla_final, tabla_destinos, num_destinos)
        
        logger.info(f"Guardando reporte en: {output}")
        libro.save(output)
        logger.info("Reporte completado exitosamente")
        
    except FileNotFoundError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.error(f"Error generando reporte: {str(e)}")
        raise


def _escribir_comercio_agro(hoja, tabla_final, tabla_destinos, num_destinos):
    """Escribe datos en la hoja Comercio_Agro."""
    try:
        # Flujos y grupos de productos
        for t in range(0, 3):
            hoja.cell(10, 8+t).value = tabla_final.iloc[0, t]
        for t in range(0, 2):
            hoja.cell(10, 13+t).value = tabla_final.iloc[0, t+4]
        
        # Grupos
        for x in range(0, 2):
            hoja.cell(11+(15*x), 6).value = _index_label(tabla_final.index[x+1])
            for t in range(0, 3):
                hoja.cell(11+(15*x), 8+t).value = tabla_final.iloc[x+1, t]
            for t in range(0, 2):
                hoja.cell(11+(15*x), 13+t).value = tabla_final.iloc[x+1, t+4]
        
        # Principales destinos
        for x in range(0, 5):
            hoja.cell(55+x, 6).value = _index_label(tabla_destinos.index[x+1])
            for t in range(0, 3):
                hoja.cell(55+x, 8+t).value = tabla_destinos.iloc[x+1, t]
            hoja.cell(55+x, 13).value = tabla_destinos.iloc[x+1, 4]
            hoja.cell(55+x, 14).value = tabla_destinos.iloc[x+1, 5]
        
        # Numero de destinos
        for t in range(0, 3):
            hoja.cell(62, 8+t).value = num_destinos.iloc[0, t]
        
        logger.debug("Hoja Comercio_Agro completada")
    except Exception as e:
        logger.error(f"Error escribiendo Comercio_Agro: {str(e)}")
        raise


def _index_label(value):
    if isinstance(value, tuple):
        for item in reversed(value):
            if item not in (None, ''):
                return str(item)
        return ''
    return str(value)


def _escribir_comercio_textil(hoja, tabla_final, tabla_destinos, num_destinos):
    """Escribe datos en la hoja Comercio_Textil."""
    try:
        # Flujos y grupos de productos
        row_map = {0: 10, 1: 12, 2: 17}
        for idx, row in row_map.items():
            for t in range(0, 3):
                hoja.cell(row, 8+t).value = tabla_final.iloc[idx, t]
            for t in range(0, 2):
                hoja.cell(row, 13+t).value = tabla_final.iloc[idx, t+4]
        
        # Principales destinos
        for x in range(0, 3):
            hoja.cell(24+x, 6).value = _index_label(tabla_destinos.index[x+1])
            for t in range(0, 3):
                hoja.cell(24+x, 8+t).value = tabla_destinos.iloc[x+1, t]
            hoja.cell(24+x, 13).value = tabla_destinos.iloc[x+1, 4]
            hoja.cell(24+x, 14).value = tabla_destinos.iloc[x+1, 5]
        
        # Numero de destinos
        for t in range(0, 3):
            hoja.cell(27, 8+t).value = num_destinos.iloc[0, t]
        
        logger.debug("Hoja Comercio_Textil completada")
    except Exception as e:
        logger.error(f"Error escribiendo Comercio_Textil: {str(e)}")
        raise


def _escribir_comercio_pesca(hoja, tabla_final, tabla_destinos, num_destinos):
    """Escribe datos en la hoja comercio_Pesca."""
    try:
        # Flujos y grupos de productos
        for t in range(0, 3):
            hoja.cell(10, 8+t).value = tabla_final.iloc[3, t]
        for t in range(0, 2):
            hoja.cell(10, 13+t).value = tabla_final.iloc[3, t+4]
        
        # Principales destinos
        for x in range(0, 4):
            hoja.cell(37+x, 6).value = _index_label(tabla_destinos.index[x+7])
            for t in range(0, 3):
                hoja.cell(37+x, 8+t).value = tabla_destinos.iloc[x+7, t]
            hoja.cell(37+x, 13).value = tabla_destinos.iloc[x+7, 4]
            hoja.cell(37+x, 14).value = tabla_destinos.iloc[x+7, 5]
        
        # Numero de destinos
        for t in range(0, 3):
            hoja.cell(41, 8+t).value = num_destinos.iloc[1, t]
        
        logger.debug("Hoja comercio_Pesca completada")
    except Exception as e:
        logger.error(f"Error escribiendo comercio_Pesca: {str(e)}")
        raise