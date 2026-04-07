import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def procesar_base(df, config):
    """Procesa la base de datos: renombra columnas, crea campos derivados, agrupa y expande periodos."""
    try:
        logger.info(f"Iniciando procesamiento de {len(df)} registros")
        
        # RENOMBRAR COLUMNAS
        df = df.rename(columns={
            'Subpartida': 'codigo_partida',
            'CPAIDES': 'cod_pais',
            'AÑO': 'año',
            'MES': 'mes',
            'NDOC': 'RUC',
            'VPESNET': 'PesoNeto',
            'FOB': 'fob',
            'Flujo': 'flujo_comercial'
        })

        # CREAR CAMPOS DERIVADOS
        df['cod_capitulo'] = df['codigo_partida'].str[:2]
        df['cuatro_dig'] = df['codigo_partida'].str[:4]

        # PRIMERA AGRUPACIÓN: consolidar por variables_a_agrupar
        variables_a_agrupar_x = ['flujo_comercial','cod_pais','cod_capitulo','codigo_partida','cuatro_dig','año','mes','CADU','RUC']
        df[variables_a_agrupar_x] = df[variables_a_agrupar_x].fillna('NaN_temp')

        base1_x = df.groupby(variables_a_agrupar_x).agg({
            'fob': 'sum',
            'PesoNeto': 'sum'
        }).reset_index()

        base1_x[variables_a_agrupar_x] = base1_x[variables_a_agrupar_x].replace('NaN_temp', np.nan)

        # CONVERTIR TIPOS
        base1_x['año'] = base1_x['año'].astype(int)
        base1_x['mes'] = base1_x['mes'].astype(int)

        # FILTRAR: eliminar datos de meses posteriores al mes actual del año actual, el ~ es para negar la condición 
        logger.debug(f"Eliminando datos posteriores a mes {config.MES_NUM[1]} del año {config.ANIOS[0]}")
        base1_x = base1_x[~((base1_x['año']==config.ANIOS[0]) & (base1_x['mes']>=config.MES_NUM[1]))]

        # CREAR VARIABLE PERIODO (PASO 1)/ loc. es para asignar valores a filas específicas según condiciones / 
        # .loc sirve para asignar valores a filas específicas según condiciones / .isin es para verificar si el valor de 'periodo' está en la lista de periodos.
        # .debug es para mostrar información detallada durante el procesamiento, útil para verificar que los periodos se asignen correctamente.
        # ,_ es para ignorar la segunda parte del resultado de construir_periodos() que no se necesita en este paso
        #perio
        base1_x['periodo'] = ''
        base1_x.loc[base1_x['año'] == config.ANIOS[1]-1, 'periodo'] = str(config.ANIOS[1]-1)
        base1_x.loc[base1_x['año'] == config.ANIOS[1], 'periodo'] = str(config.ANIOS[1])
        
        periodo_crear, _ = config.construir_periodos()
        base1_x.loc[base1_x['año'] == config.ANIOS[0], 'periodo'] = periodo_crear[1]

        logger.debug(f"Base1 completada: {len(base1_x)} registros con periodos")

        # SEGUNDA AGRUPACIÓN: crear periodos "Acumulado" y "Últimos 12 meses" / .copy sirve para crear una copia del DataFrame filtrado, evitando advertencias de pandas sobre asignaciones a vistas de DataFrames.
        base2_x = base1_x[(base1_x['año']==config.ANIOS[1]) | (base1_x['año']==config.ANIOS[0])].copy()
        
        # Asignar periodos acumulados
        base2_x.loc[(base2_x['año']==config.ANIOS[1]) & (base2_x['mes']<=config.MES_NUM[0]), 'periodo'] = periodo_crear[0]
        base2_x.loc[((base2_x['año']==config.ANIOS[1]) & (base2_x['mes']>=config.MES_NUM[1])) | 
                    ((base2_x['año']==config.ANIOS[0]) & (base2_x['mes']<=config.MES_NUM[0])), 'periodo'] = periodo_crear[2]
        
        # Marcar año como 0 para evitar duplicados
        base2_x.loc[:, 'año'] = 0

        logger.debug(f"Base2 completada: {len(base2_x)} registros con periodos acumulados")

        # CONCATENAR BASES
        data_final_x = pd.concat([base1_x, base2_x], axis=0, ignore_index=True)

        # TERCERA AGRUPACIÓN: consolidar por periodos
        variables_a_agrupar2_x = ['flujo_comercial','cod_pais','cod_capitulo','codigo_partida','cuatro_dig','año','CADU','RUC','periodo']
        data_final_x[variables_a_agrupar2_x] = data_final_x[variables_a_agrupar2_x].fillna('NaN_temp')

        data_final_x = data_final_x.groupby(variables_a_agrupar2_x).agg({
            'fob': 'sum',
            'PesoNeto': 'sum'
        }).reset_index()

        data_final_x[variables_a_agrupar2_x] = data_final_x[variables_a_agrupar2_x].replace('NaN_temp', np.nan)

        logger.info(f"Procesamiento completado. {len(data_final_x)} registros con {data_final_x['periodo'].nunique()} períodos")
        return data_final_x
    except Exception as e:
        logger.error(f"Error en procesar_base: {str(e)}")
        raise



# "&" es para combinar condiciones, "|" es para "o" lógico , "~" es para negar la condición.