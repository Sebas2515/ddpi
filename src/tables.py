import pandas as pd
import logging

logger = logging.getLogger(__name__)

def tabla_sectorial(df, sector, periodos, periodos_miles_TM):
    """Crea tabla pivote sectorial básica (nivel sector)."""
    try:
        logger.info(f"Generando tabla sectorial para {sector}")
        datos_filtrados = df[(df['sector2']==sector) & (df['periodo'].isin(periodos))]
        
        if datos_filtrados.empty:
            logger.warning(f"Sin datos para sector {sector}")
            return pd.DataFrame()
        
        tabla = datos_filtrados.pivot_table(
            index=['flujo_comercial', 'flujo_comercial2', 'flujo_comercial3', 'sector2'],
            columns='periodo',
            values=['millones_fob','miles_TM'],
            aggfunc='sum'
        )
        
        # Seleccionar columnas relevantes
        columnas_miles_TM = [col for col in tabla.columns if col[1] in periodos_miles_TM and col[0]=='miles_TM']
        columnas_millones_fob = [col for col in tabla.columns if col[0]=='millones_fob']
        tabla_final = tabla[columnas_millones_fob + columnas_miles_TM]
        
        logger.info(f"Tabla sectorial generada: {tabla_final.shape}")
        return tabla_final
    except Exception as e:
        logger.error(f"Error en tabla_sectorial: {str(e)}")
        raise

def tabla_grupos(df, sector, grupos, periodos, periodos_miles_TM):
    """Crea tabla pivote de grupos dentro de un sector."""
    try:
        logger.info(f"Generando tabla de grupos para {sector}")
        tablas_grupos = pd.DataFrame()
        
        for grupo in grupos:
            datos_filtrados = df[(df['grupo2']==grupo) & (df['sector2']==sector) & (df['periodo'].isin(periodos))]
            
            if datos_filtrados.empty:
                continue
            
            tabla_grupo = datos_filtrados.pivot_table(
                index=['flujo_comercial2', 'flujo_comercial3', 'sector2', 'grupo2'],
                columns='periodo',
                values=['millones_fob','miles_TM'],
                aggfunc='sum'
            )
            
            columnas_miles_TM = [col for col in tabla_grupo.columns if col[1] in periodos_miles_TM and col[0]=='miles_TM']
            columnas_millones_fob = [col for col in tabla_grupo.columns if col[0]=='millones_fob']
            tabla_grupo_final = tabla_grupo[columnas_millones_fob + columnas_miles_TM]
            
            tablas_grupos = pd.concat([tablas_grupos, tabla_grupo_final])
        
        logger.info(f"Tabla de grupos generada: {tablas_grupos.shape}")
        return tablas_grupos
    except Exception as e:
        logger.error(f"Error en tabla_grupos: {str(e)}")
        raise

def tabla_productos(df, sector, grupo, productos, periodos, periodos_miles_TM, periodo_orden):
    """Crea tabla pivote de productos dentro de un grupo."""
    try:
        logger.info(f"Generando tabla de productos para {grupo} en {sector}")
        tablas_productos = pd.DataFrame()
        
        for producto in productos:
            datos_filtrados = df[(df['producto2']==producto) & (df['grupo2']==grupo) & 
                                (df['sector2']==sector) & (df['periodo'].isin(periodos))]
            
            if datos_filtrados.empty:
                continue
            
            tabla_prod = datos_filtrados.pivot_table(
                index=['flujo_comercial', 'sector2', 'grupo2', 'producto2'],
                columns='periodo',
                values=['millones_fob','miles_TM'],
                aggfunc='sum'
            )
            tabla_prod = tabla_prod.sort_values(by=('millones_fob', periodo_orden), ascending=False)
            
            tabla_prod_producto = datos_filtrados.pivot_table(
                index=['sector2', 'grupo2', 'producto2', 'producto21'],
                columns='periodo',
                values=['millones_fob','miles_TM'],
                aggfunc='sum'
            )
            tabla_prod_producto = tabla_prod_producto.sort_values(by=('millones_fob', periodo_orden), ascending=False).head(3)
            
            columnas_miles_TM_p = [col for col in tabla_prod.columns if col[1] in periodos_miles_TM and col[0]=='miles_TM']
            columnas_miles_TM_pp = [col for col in tabla_prod_producto.columns if col[1] in periodos_miles_TM and col[0]=='miles_TM']
            columnas_millones_fob_p = [col for col in tabla_prod.columns if col[0]=='millones_fob']
            columnas_millones_fob_pp = [col for col in tabla_prod_producto.columns if col[0]=='millones_fob']
            
            tabla_prods = tabla_prod[columnas_millones_fob_p + columnas_miles_TM_p]
            tabla_productos_final = tabla_prod_producto[columnas_millones_fob_pp + columnas_miles_TM_pp]
            
            tablas_productos = pd.concat([tablas_productos, tabla_prods, tabla_productos_final])
        
        logger.info(f"Tabla de productos generada: {tablas_productos.shape}")
        return tablas_productos
    except Exception as e:
        logger.error(f"Error en tabla_productos: {str(e)}")
        raise


def detalle_textil(df, periodos, periodos_miles_TM):
    """Construye el detalle de productos esperado por la plantilla de Comercio_Textil."""
    try:
        logger.info("Generando detalle de productos para Textil")
        data_textil = df[(df['sector2']=='Textil') & (df['periodo'].isin(periodos))]

        definiciones = {
            'prendas_vestir': (
                (data_textil['grupo2']=='Confecciones') &
                (data_textil['producto2']=='Prendas de vestir')
            ),
            'prendas_algodon': (
                (data_textil['grupo2']=='Confecciones') &
                (data_textil['producto2']=='Prendas de vestir') &
                (data_textil['producto21']=='Algodón')
            ),
            'mantas_pelo_fino': (
                (data_textil['grupo2']=='Confecciones') &
                (data_textil['producto2']=='Otras confecciones') &
                (data_textil['producto21']=='Lana y pelo fino')
            ),
            'mantas_algodon': (
                (data_textil['grupo2']=='Confecciones') &
                (data_textil['producto2']=='Otras confecciones') &
                (data_textil['producto21']=='Mantas de algodón') &
                (data_textil['codigo_partida']=='6301300000')    
            ),
            'fibras_textiles': (
                (data_textil['grupo2']=='Textiles') &
                (data_textil['producto2']=='Fibras textiles')
            ),
            'tejidos': (
                (data_textil['grupo2']=='Textiles') &
                (data_textil['producto2']=='Tejidos')
            ),
            'tejidos_algodon': (
                (data_textil['grupo2']=='Textiles') &
                (data_textil['producto2']=='Tejidos') &
                (data_textil['producto21']=='Algodón')
            ),
            'hilos_hilados': (
                (data_textil['grupo2']=='Textiles') &
                (data_textil['producto2']=='Hilos e Hilados')
            ),
        }

        filas = []
        for etiqueta, filtro in definiciones.items():
            serie = _resumen_periodos(data_textil[filtro], periodos, periodos_miles_TM)
            serie.name = etiqueta
            filas.append(serie)

        resultado = pd.DataFrame(filas)
        logger.info(f"Detalle de productos textil generado: {resultado.shape}")
        return resultado
    except Exception as e:
        logger.error(f"Error en detalle_textil: {str(e)}")
        raise


def detalle_textil_importaciones(df, periodos, periodos_miles_TM):
    """Construye el detalle de importaciones esperado por Comercio_Textil."""
    try:
        logger.info("Generando detalle de productos para importaciones de Textil")
        data_textil = df[(df['sector2']=='Textil') & (df['periodo'].isin(periodos))]

        materiales_sinteticos = [
            'sinteticas',
            'sinteticas y artificiales',
            'Artificiales',
            'Acrilicas o modacrilicas',
            'Acrilicos o modacrilicos',
            'Nailon y demás poliamidas',
            'Poliamidas',
            'Poliuretano',
            'Polipropileno',
            'Poliester',
        ]

        definiciones = {
            'sector_total': pd.Series(True, index=data_textil.index),
            'textiles': data_textil['grupo2']=='Textiles',
            'tejidos': (
                (data_textil['grupo2']=='Textiles') &
                (data_textil['producto2']=='Tejidos')
            ),
            'tejidos_poliester': (
                (data_textil['grupo2']=='Textiles') &
                (data_textil['producto2']=='Tejidos') &
                (data_textil['producto21']=='Poliester')
            ),
            'tejidos_algodon': (
                (data_textil['grupo2']=='Textiles') &
                (data_textil['producto2']=='Tejidos') &
                (data_textil['producto21']=='Algodón')
            ),
            'hilos_hilados': (
                (data_textil['grupo2']=='Textiles') &
                (data_textil['producto2']=='Hilos e Hilados')
            ),
            'hilos_algodon': (
                (data_textil['grupo2']=='Textiles') &
                (data_textil['producto2']=='Hilos e Hilados') &
                (data_textil['producto21']=='Algodón')
            ),
            'fibras_textiles': (
                (data_textil['grupo2']=='Textiles') &
                (data_textil['producto2']=='Fibras textiles')
            ),
            'confecciones': data_textil['grupo2']=='Confecciones',
            'prendas_vestir': (
                (data_textil['grupo2']=='Confecciones') &
                (data_textil['producto2']=='Prendas de vestir')
            ),
            'prendas_algodon': (
                (data_textil['grupo2']=='Confecciones') &
                (data_textil['producto2']=='Prendas de vestir') &
                (data_textil['producto21']=='Algodón')
            ),
            'prendas_sinteticas': (
                (data_textil['grupo2']=='Confecciones') &
                (data_textil['producto2']=='Prendas de vestir') &
                (data_textil['producto21'].isin(materiales_sinteticos))
            ),
            'otras_confecciones': (
                (data_textil['grupo2']=='Confecciones') &
                (data_textil['producto2']=='Otras confecciones')
            ),
            'mantas_fibra_sintetica': (
                (data_textil['grupo2']=='Confecciones') &
                (data_textil['producto2']=='Otras confecciones') &
                (data_textil['codigo_partida']=='6301400000')
            ),
            'ropa_de_cama': (
                (data_textil['grupo2']=='Confecciones') &
                (data_textil['producto2']=='Otras confecciones') &
                (data_textil['producto21']=='Ropa de cama')
            ),
        }

        filas = []
        for etiqueta, filtro in definiciones.items():
            serie = _resumen_periodos(data_textil[filtro], periodos, periodos_miles_TM)
            serie.name = etiqueta
            filas.append(serie)

        resultado = pd.DataFrame(filas)
        logger.info(f"Detalle de importaciones textil generado: {resultado.shape}")
        return resultado
    except Exception as e:
        logger.error(f"Error en detalle_textil_importaciones: {str(e)}")
        raise


def _resumen_periodos(df_filtrado, periodos, periodos_miles_TM):
    """Resume FOB y TM por período en el orden esperado por la plantilla."""
    columnas = (
        [('millones_fob', periodo) for periodo in periodos] +
        [('miles_TM', periodo) for periodo in periodos_miles_TM]
    )

    if df_filtrado.empty:
        return pd.Series([None] * len(columnas), index=columnas, dtype='object')

    resumen = df_filtrado.groupby('periodo')[['millones_fob', 'miles_TM']].sum()
    valores = []

    for periodo in periodos:
        valor = resumen.loc[periodo, 'millones_fob'] if periodo in resumen.index else None
        valores.append(valor)

    for periodo in periodos_miles_TM:
        valor = resumen.loc[periodo, 'miles_TM'] if periodo in resumen.index else None
        valores.append(valor)

    return pd.Series(valores, index=columnas, dtype='object')

def ranking_destinos(df, sector, periodos, periodos_miles_TM, periodo_orden):
    """Genera ranking de top 5 destinos por sector."""
    try:
        logger.info(f"Generando ranking de destinos para {sector}")
        data_filtrada = df[(df['sector2']==sector) & (df['periodo'].isin(periodos))]
        
        if data_filtrada.empty:
            logger.warning(f"Sin datos para ranking de {sector}")
            return pd.DataFrame()
        
        tabla_sector = data_filtrada.pivot_table(
            index='sector2',
            columns='periodo',
            values=['millones_fob','miles_TM'],
            aggfunc='sum'
        )
        tabla_sector = tabla_sector.sort_values(by=('millones_fob', periodo_orden), ascending=False)
        
        tabla_paises = data_filtrada.pivot_table(
            index='Pais_UE27',
            columns='periodo',
            values=['millones_fob','miles_TM'],
            aggfunc='sum'
        )
        tabla_paises = tabla_paises.sort_values(by=('millones_fob', periodo_orden), ascending=False).head(5)
        
        columnas_miles_TM_s = [col for col in tabla_sector.columns if col[1] in periodos_miles_TM and col[0]=='miles_TM']
        columnas_miles_TM_p = [col for col in tabla_paises.columns if col[1] in periodos_miles_TM and col[0]=='miles_TM']
        columnas_millones_fob_s = [col for col in tabla_sector.columns if col[0]=='millones_fob']
        columnas_millones_fob_p = [col for col in tabla_paises.columns if col[0]=='millones_fob']
        
        tabla_sectores = tabla_sector[columnas_millones_fob_s + columnas_miles_TM_s]
        tabla_paises_final = tabla_paises[columnas_millones_fob_p + columnas_miles_TM_p]
        
        tabla_final = pd.concat([tabla_sectores, tabla_paises_final])
        logger.info(f"Ranking de destinos generado: {tabla_final.shape}")
        return tabla_final
    except Exception as e:
        logger.error(f"Error en ranking_destinos: {str(e)}")
        raise

def numero_destinos(df, sectores, periodos):
    """Calcula número único de países por sector y período."""
    try:
        logger.info("Calculando número de destinos por sector")
        resultado = df[(df['periodo'].isin(periodos)) & (df['sector2'].isin(sectores)) & 
                      (df['millones_fob'] > 0)].groupby(['sector2', 'periodo']).agg(
                          Numero_Destinos=('Pais', 'nunique')).unstack()
        logger.info(f"Número de destinos calculado: {resultado.shape}")
        return resultado
    except Exception as e:
        logger.error(f"Error en numero_destinos: {str(e)}")
        raise


def ranking_proveedores(df, sector, periodos, periodos_miles_TM, periodo_orden, top_n=4):
    """Genera ranking de principales proveedores (importaciones) por sector."""
    try:
        logger.info(f"Generando ranking de proveedores para {sector}")
        data_filtrada = df[(df['sector2'] == sector) & (df['periodo'].isin(periodos))]

        if data_filtrada.empty:
            logger.warning(f"Sin datos para ranking de proveedores de {sector}")
            return pd.DataFrame()

        tabla_sector = data_filtrada.pivot_table(
            index='sector2',
            columns='periodo',
            values=['millones_fob', 'miles_TM'],
            aggfunc='sum',
        )
        tabla_sector = tabla_sector.sort_values(by=('millones_fob', periodo_orden), ascending=False)

        tabla_paises = data_filtrada.pivot_table(
            index='Pais_UE27',
            columns='periodo',
            values=['millones_fob', 'miles_TM'],
            aggfunc='sum',
        )
        tabla_paises = tabla_paises.sort_values(by=('millones_fob', periodo_orden), ascending=False).head(top_n)

        columnas_miles_TM_s = [col for col in tabla_sector.columns if col[1] in periodos_miles_TM and col[0] == 'miles_TM']
        columnas_miles_TM_p = [col for col in tabla_paises.columns if col[1] in periodos_miles_TM and col[0] == 'miles_TM']
        columnas_millones_fob_s = [col for col in tabla_sector.columns if col[0] == 'millones_fob']
        columnas_millones_fob_p = [col for col in tabla_paises.columns if col[0] == 'millones_fob']

        tabla_sectores = tabla_sector[columnas_millones_fob_s + columnas_miles_TM_s]
        tabla_paises_final = tabla_paises[columnas_millones_fob_p + columnas_miles_TM_p]

        tabla_final = pd.concat([tabla_sectores, tabla_paises_final])
        logger.info(f"Ranking de proveedores generado: {tabla_final.shape}")
        return tabla_final
    except Exception as e:
        logger.error(f"Error en ranking_proveedores: {str(e)}")
        raise


def numero_proveedores(df, sectores, periodos):
    """Calcula número único de proveedores (países) por sector y período."""
    try:
        logger.info("Calculando número de proveedores por sector")
        resultado = df[
            (df['periodo'].isin(periodos))
            & (df['sector2'].isin(sectores))
            & (df['millones_fob'] > 0)
        ].groupby(['sector2', 'periodo']).agg(
            Numero_Proveedores=('Pais', 'nunique')
        ).unstack()
        logger.info(f"Número de proveedores calculado: {resultado.shape}")
        return resultado
    except Exception as e:
        logger.error(f"Error en numero_proveedores: {str(e)}")
        raise
