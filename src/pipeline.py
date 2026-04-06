from src.data_loader import cargar_base, cargar_correlaciones
from src.processing import procesar_base
from src.transformations import aplicar_transformaciones
from src.tables import tabla_sectorial, tabla_grupos, tabla_productos, ranking_destinos, numero_destinos
from src.excel_writer import generar_reporte
from src.indices_generator import generar_indices
import src.config as config
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def run_pipeline():
    """Ejecuta el pipeline completo de carga, procesamiento y exportación."""
    try:
        logger.info("="*70)
        logger.info("INICIANDO PIPELINE DE PROCESAMIENTO RMC")
        logger.info("="*70)

        logger.info("📥 Cargando datos...")
        df = cargar_base(config)

        logger.info("🔗 Cargando correlaciones...")
        c_pais, c_prod, c_cap = cargar_correlaciones(config)

        logger.info("🧹 Procesando base...")
        df = procesar_base(df, config)

        logger.info("🔄 Aplicando transformaciones...")
        df = aplicar_transformaciones(df, c_pais, c_prod, c_cap)
        
        # Agregar columnas necesarias para generar tablas
        df.insert(1, 'flujo_comercial2', 'EXPORTACION')
        df.insert(2, 'flujo_comercial3', 'EXPORTACION')

        # Construir períodos
        periodo_crear, periodos = config.construir_periodos()
        periodos_miles_TM = [periodo_crear[0], periodo_crear[1]]
        periodo_ordenar = periodo_crear[2]
        
        logger.info(f"Períodos configurados: {periodos}")
        logger.info(f"Período para ordenar: {periodo_ordenar}")

        # GENERAR TABLAS SECTORIALES PARA AGRO
        logger.info("📊 Generando tablas para Textil/Confecciones...")
        sectores_a_procesar = ['Textil']
        
        tabla_final = pd.DataFrame()
        for sector in sectores_a_procesar:
            tabla_1 = tabla_sectorial(df, sector, periodos, periodos_miles_TM)
            
            flujo_grupo = df[(df['sector2']==sector) & (df['periodo']==periodo_ordenar)].groupby('grupo2')['millones_fob'].sum()
            flujo_grupo_ordenado = flujo_grupo.sort_values(ascending=False)
            grupos = [g for g in flujo_grupo_ordenado.index if g != "NA"][:2]
            
            tabla_3 = tabla_grupos(df[df['sector2']==sector], sector, grupos, periodos, periodos_miles_TM)
            tabla_5 = pd.concat([tabla_1, tabla_3])
            tabla_final = pd.concat([tabla_final, tabla_5])
        
        logger.info(f"Tabla final generada: {tabla_final.shape}")

        # RANKING DE DESTINOS POR SECTOR
        logger.info("🌍 Generando ranking de destinos...")
        tabla_destinos = pd.DataFrame()
        for sector in sectores_a_procesar:
            tabla_rank = ranking_destinos(df, sector, periodos, periodos_miles_TM, periodo_ordenar)
            tabla_destinos = pd.concat([tabla_destinos, tabla_rank])
        
        logger.info(f"Ranking de destinos generado: {tabla_destinos.shape}")

        # NUMERO DE DESTINOS
        logger.info("📍 Calculando número de destinos...")
        num_destinos_sect = numero_destinos(df, sectores_a_procesar, periodos)
        logger.info(f"Número de destinos: {num_destinos_sect.shape}")

        # GENERAR INDICES
        logger.info("📈 Generando índices...")
        indices = generar_indices(df, sectores_a_procesar, periodos, periodo_ordenar)

        # EXPORTAR A EXCEL
        logger.info("📤 Exportando a Excel...")
        tablas_dict = {
            'tabla_final': tabla_final,
            'tabla_destinos': tabla_destinos,
            'num_destinos': num_destinos_sect
        }
        
        generar_reporte(tablas_dict, indices, config)

        logger.info("="*70)
        logger.info("✅ PIPELINE COMPLETADO EXITOSAMENTE")
        logger.info("="*70)
        
        return df

    except Exception as e:
        logger.error(f"\n❌ ERROR EN PIPELINE: {str(e)}\n")
        raise

