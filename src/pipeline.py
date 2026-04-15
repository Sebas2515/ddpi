import logging

import pandas as pd

import src.config as config
from src.data_loader import cargar_bases, cargar_correlaciones
from src.excel_writer import generar_reporte
from src.indices_generator import generar_indices, generar_indices_importaciones_textil
from src.processing import procesar_base
from src.tables import (
    detalle_textil,
    detalle_textil_importaciones,
    numero_destinos,
    numero_proveedores,
    ranking_destinos,
    ranking_proveedores,
    tabla_grupos,
    tabla_sectorial,
)
from src.transformations import aplicar_transformaciones

logger = logging.getLogger(__name__)


def run_pipeline():
    """Ejecuta el pipeline completo de exportaciones e importaciones."""
    try:
        logger.info("=" * 70)
        logger.info("INICIANDO PIPELINE DE PROCESAMIENTO RMC")
        logger.info("=" * 70)

        logger.info("Cargando datos...")
        bases = cargar_bases(config)
        df_expo = bases['exportaciones']
        df_impo = bases['importaciones']

        logger.info("Cargando correlaciones...")
        c_pais, c_prod, c_cap = cargar_correlaciones(config)

        logger.info("Procesando base de exportaciones...")
        df_expo = procesar_base(df_expo, config)
        logger.info("Aplicando transformaciones a exportaciones...")
        df_expo = aplicar_transformaciones(df_expo, c_pais, c_prod, c_cap)
        df_expo.insert(1, 'flujo_comercial2', 'EXPORTACION')
        df_expo.insert(2, 'flujo_comercial3', 'EXPORTACION')

        logger.info("Procesando base de importaciones...")
        df_impo = procesar_base(df_impo, config)
        logger.info("Aplicando transformaciones a importaciones...")
        df_impo = aplicar_transformaciones(df_impo, c_pais, c_prod, c_cap)
        df_impo.insert(1, 'flujo_comercial2', 'IMPORTACION')
        df_impo.insert(2, 'flujo_comercial3', 'IMPORTACION')

        periodo_crear, periodos = config.construir_periodos()
        periodos_miles_tm = [periodo_crear[0], periodo_crear[1]]
        periodo_ordenar = periodo_crear[2]

        logger.info(f"Periodos configurados: {periodos}")
        logger.info(f"Periodo para ordenar: {periodo_ordenar}")

        sectores_a_procesar = ['Textil']

        logger.info("Generando tablas de exportaciones para Textil/Confecciones...")
        tabla_final = pd.DataFrame()
        for sector in sectores_a_procesar:
            tabla_sector = tabla_sectorial(df_expo, sector, periodos, periodos_miles_tm)

            flujo_grupo = df_expo[
                (df_expo['sector2'] == sector) &
                (df_expo['periodo'] == periodo_ordenar)
            ].groupby('grupo2')['millones_fob'].sum()
            grupos = [g for g in flujo_grupo.sort_values(ascending=False).index if g != "NA"][:2]

            tabla_grupo = tabla_grupos(
                df_expo[df_expo['sector2'] == sector],
                sector,
                grupos,
                periodos,
                periodos_miles_tm,
            )
            tabla_final = pd.concat([tabla_final, tabla_sector, tabla_grupo])

        logger.info(f"Tabla final de exportaciones generada: {tabla_final.shape}")

        logger.info("Generando detalle de exportaciones textil...")
        tabla_detalle_textil = detalle_textil(df_expo, periodos, periodos_miles_tm)

        logger.info("Generando detalle de importaciones textil...")
        tabla_detalle_textil_import = detalle_textil_importaciones(df_impo, periodos, periodos_miles_tm)

        logger.info("Generando ranking de destinos de exportaciones...")
        tabla_destinos = pd.DataFrame()
        for sector in sectores_a_procesar:
            tabla_rank = ranking_destinos(df_expo, sector, periodos, periodos_miles_tm, periodo_ordenar)
            tabla_destinos = pd.concat([tabla_destinos, tabla_rank])
        logger.info(f"Ranking de destinos generado: {tabla_destinos.shape}")

        logger.info("Calculando numero de destinos de exportaciones...")
        num_destinos_sect = numero_destinos(df_expo, sectores_a_procesar, periodos)
        logger.info(f"Numero de destinos: {num_destinos_sect.shape}")

        logger.info("Generando ranking de proveedores de importaciones...")
        tabla_proveedores = pd.DataFrame()
        for sector in sectores_a_procesar:
            tabla_rank = ranking_proveedores(df_impo, sector, periodos, periodos_miles_tm, periodo_ordenar, top_n=4)
            tabla_proveedores = pd.concat([tabla_proveedores, tabla_rank])
        logger.info(f"Ranking de proveedores generado: {tabla_proveedores.shape}")

        logger.info("Calculando numero de proveedores de importaciones...")
        num_proveedores_sect = numero_proveedores(df_impo, sectores_a_procesar, periodos)
        logger.info(f"Numero de proveedores: {num_proveedores_sect.shape}")

        logger.info("Generando indices de exportaciones...")
        indices = generar_indices(df_expo, sectores_a_procesar, periodos, periodo_ordenar)

        logger.info("Generando indices de importaciones...")
        indices['indice_textil_import'] = generar_indices_importaciones_textil(
            df_impo,
            periodos,
            periodo_ordenar,
        )

        logger.info("Exportando a Excel...")
        tablas_dict = {
            'tabla_final': tabla_final,
            'detalle_textil': tabla_detalle_textil,
            'detalle_textil_import': tabla_detalle_textil_import,
            'tabla_destinos': tabla_destinos,
            'num_destinos': num_destinos_sect,
            'tabla_proveedores': tabla_proveedores,
            'num_proveedores': num_proveedores_sect,
        }

        generar_reporte(tablas_dict, indices, config)

        logger.info("=" * 70)
        logger.info("PIPELINE COMPLETADO EXITOSAMENTE")
        logger.info("=" * 70)

        return {
            'exportaciones': df_expo,
            'importaciones': df_impo,
        }

    except Exception as e:
        logger.error(f"\nERROR EN PIPELINE: {str(e)}\n")
        raise
