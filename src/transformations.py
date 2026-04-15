import pandas as pd
import logging

logger = logging.getLogger(__name__)

def aplicar_transformaciones(df, correlac_pais, correlac_prod, correlac_cap):
    """Aplica transformaciones y merges con tablas de correlación."""
    try:
        logger.info("Iniciando transformaciones...")
        
        # Asegurar que los campos usados en los merges sean texto y tengan formato consistente.
        df['cod_pais'] = df['cod_pais'].astype(str)
        df['codigo_partida'] = df['codigo_partida'].astype(str).str.zfill(10)
        df['cuatro_dig'] = df['cuatro_dig'].astype(str).str.zfill(4)

        correlac_pais['cod_pais'] = correlac_pais['cod_pais'].astype(str)
        correlac_prod['codigo_partida'] = correlac_prod['codigo_partida'].astype(str).str.zfill(10)
        correlac_cap['cuatro_dig'] = correlac_cap['cuatro_dig'].astype(str).str.zfill(4)

        # Evitar colisiones de columna: correlac_prod también tiene cuatro_dig, pero lo usaremos solo en correlac_cap.
        correlac_prod = correlac_prod.drop(columns=['cuatro_dig'], errors='ignore')

        df = df.merge(correlac_pais, on='cod_pais', how='left')
        logger.debug(f"Merge país completado: {len(df)} registros")
        
        df = df.merge(correlac_prod, on='codigo_partida', how='left')
        logger.debug(f"Merge producto completado: {len(df)} registros")
        
        df = df.merge(correlac_cap, on='cuatro_dig', how='left')
        logger.debug(f"Merge capítulo completado: {len(df)} registros")

        df['cinco_dig'] = df['codigo_partida'].str[:5]

        # VARIABLES MONETARIAS
        df['millones_fob'] = df['fob'] / 1_000_000
        df['miles_TM'] = df['PesoNeto'] / 1_000_000

        # ===== TRANSFORMACIONES COMPLETAS =====

        # PRODUCTO2 - Clasificación refinada por sector
        df['producto2'] = df['Producto']
        
        # Textil/Confecciones
        df.loc[df['Sector']=='Textil', 'producto2'] = df['Familia_Textil']
        df.loc[(df['Sector']=='Textil') & (df['producto2']=='fibras'), 'producto2'] = 'Fibras textiles'
        df.loc[(df['Sector']=='Textil') & (df['producto2']=='Otras prendas'), 'producto2'] = 'Otras confecciones'
        #df.loc[(df['Sector']=='Textil') & (df['Producto']=='Otras prendas') & ((df['Familia_Textil']=='Algodón')| (df['codigo_partida']=='6301300000') ), 'producto2'] = 'Mantas de algodón'
        
        # Metalúrgico
        df.loc[df['Producto']=='Zinc refinado', 'producto2'] = 'Lingotes de zinc - JUMBO'
        df.loc[df['Producto']=='Plata aleada', 'producto2'] = 'Barras de plata'
        df.loc[(df['Producto']=='Barras y perfiles de cobre') & ((df['codigo_partida']=='7407100000') | 
               (df['codigo_partida']=='7407290000')), 'producto2'] = 'Barras de cobre'
        df.loc[(df['codigo_partida']=='7604292000') | (df['codigo_partida']=='7604210000') | 
               (df['codigo_partida']=='7604102000'), 'producto2'] = 'Perfiles de aluminio'
        
        # Siderúrgico
        df.loc[df['Producto']=='Construcciones y sus partes ', 'producto2'] = 'Estructuras metálicas'
        df.loc[df['cuatro_dig']=='7204', 'producto2'] = 'Chatarra'
        
        # Químico
        df.loc[df['Producto']=='Productos farmacéuticos - Medicamentos', 'producto2'] = 'Medicamentos'
        df.loc[df['Grupo']=='Plástico-manufactura', 'producto2'] = 'Plásticos-Manufacturas'
        
        # Otros
        df.loc[((df['codigo_partida']=='4410190000') | (df['codigo_partida']=='4410110000') | 
                (df['codigo_partida']=='4407199000') | (df['codigo_partida']=='4411140000') | 
                (df['codigo_partida']=='4411130000')) & (df['Sector']=='Maderas y papeles'), 
               'producto2'] = 'Tableros de madera'
        df.loc[(df['codigo_partida']=='2309909000') & (df['Sector']=='Agropecuario'), 'producto2'] = 'Alimento para langostino'

        # PRODUCTO21 - Clasificación pesquera y textil adicional
        df['producto21'] = df['producto2']
        df.loc[df['Sector']=='Pesquero', 'producto21'] = df['Clasific_pesquero']
        df.loc[df['Sector']=='Textil', 'producto21'] = df['Material_Textil']
        df.loc[
            (df['Sector']=='Textil') &
            (df['codigo_partida']=='6301300000'),
            'producto21'
        ] = 'Mantas de algodón'
        df.loc[
            (df['Sector']=='Textil') &
            (df['producto2']=='Otras confecciones') &
            (df['Producto_Textil'].fillna('').str.contains('ropa de cama', case=False, na=False)),
            'producto21'
        ] = 'Ropa de cama'    

        # PRODUCTO3 - Para análisis de familia textil
        df['producto3'] = df['producto2']
        df.loc[df['Sector']=='Textil', 'producto3'] = df['Familia_Textil']
        df.loc[(df['Rubro_Textil'].isin(['Textiles', 'Otros'])) & (df['Sector']=='Textil'), 
               'producto3'] = 'Materias textiles'

        # GRUPO2 - Agrupación principal
        df['grupo2'] = df['Grupo']
        df.loc[df['Sector']=='Siderúrgico', 'grupo2'] = 'Siderúrgico'
        df.loc[df['Sector']=='Metalúrgico', 'grupo2'] = 'Metalúrgico'
        df.loc[df['cod_capitulo']=='39', 'grupo2'] = 'Plástico'
        df.loc[df['Grupo']=='Farmacia', 'grupo2'] = 'Farmacia'
        df.loc[df['Grupo']=='Fertilizantes', 'grupo2'] = 'Fertilizantes'
        
        # Pesquero - Pescado
        df.loc[(((df['cuatro_dig']=='0302') | (df['cuatro_dig']=='0303') | (df['cuatro_dig']=='0304') | 
                 (df['cuatro_dig']=='0305') | (df['Producto']=='Conserva de pescado')) & 
                ((df['cinco_dig']!='03029') & (df['cinco_dig']!='03039') & (df['cinco_dig']!='03052') & 
                 (df['cinco_dig']!='03057'))) & (df['Sector']=='Pesquero'), 'grupo2'] = 'Pescado'
        
        # Textil
        df.loc[(df['Rubro_Textil']=='Prendas') & (df['Sector']=='Textil'), 'grupo2'] = 'Confecciones'
        df.loc[(df['Rubro_Textil'].isin(['Textiles', 'Otros'])) & (df['Sector']=='Textil'), 'grupo2'] = 'Textiles'
        
        
        # Agro
        df.loc[df['Grupo']=='Frutas', 'grupo2'] = 'Frutas'
        df.loc[df['Grupo']=='Hortalizas', 'grupo2'] = 'Hortalizas'
        
        # Pesquero - Productos
        df.loc[((df['Producto']=='Harina de pescado') | (df['Producto']=='Aceite de pescado')) & 
               (df['Sector']=='Pesquero'), 'grupo2'] = 'Productos de anchoveta'

        # GRUPO3 - Agrupación detallada
        df['grupo3'] = df['Grupo']
        
        # Acero y metalurgia
        df.loc[(df['Industria_acero'].isin(['Acero largo', 'Acero plano', 'otros acero'])) & 
               ((df['Sector']=='Siderúrgico') | (df['Sector']=='Metal mecánico')), 
               'grupo3'] = 'Productos de acero-total'
        
        # Plástico y cerámica
        df.loc[(df['cod_capitulo']=='39') & (df['Sector']=='Químico'), 'grupo3'] = 'Plástico'
        df.loc[df['cod_capitulo']=='69', 'grupo3'] = 'Productos cerámicos'
        
        # Papel, vidrio e hidrocarburos
        df.loc[df['cod_capitulo']=='48', 'grupo3'] = 'Papel y cartón'
        df.loc[df['Sector']=='Vidrio y sus manufacturas', 'grupo3'] = 'Vidrios y manufacturas'
        df.loc[df['Sector']=='Petróleo y gas natural', 'grupo3'] = 'Hidrocarburos'
        
        # Agro
        df.loc[(df['cod_capitulo']=='10') & (df['Sector']=='Agropecuario'), 'grupo3'] = 'Cereales'
        
        # Químico - Tocador y limpieza
        df.loc[((df['cod_capitulo']=='33') | (df['cod_capitulo']=='34')) & (df['Sector']=='Químico'), 
               'grupo3'] = 'Productos de tocador y limpieza'
        
        # Textil
        df.loc[df['Sector']=='Textil', 'grupo3'] = 'Textil-confecciones'
        
        # Pesquero - Pescado
        df.loc[(((df['cuatro_dig']=='0302') | (df['cuatro_dig']=='0303') | (df['cuatro_dig']=='0304') | 
                 (df['cuatro_dig']=='0305') | (df['Producto']=='Conserva de pescado')) & 
                ((df['cinco_dig']!='03029') & (df['cinco_dig']!='03039') & (df['cinco_dig']!='03052') & 
                 (df['cinco_dig']!='03057'))) & (df['Sector']=='Pesquero'), 'grupo3'] = 'Pescado'
        
        # Pesquero - Anchoveta
        df.loc[((df['Producto']=='Harina de pescado') | (df['Producto']=='Aceite de pescado')) & 
               (df['Sector']=='Pesquero'), 'grupo3'] = 'Productos de anchoveta'
        
        # Pesquero - Otros
        df.loc[((df['grupo2']!='Pescado') & (df['grupo2']!='Productos de anchoveta') & (df['Producto']!='Pota') & 
                (df['Producto']!='Langostino') & (df['Producto']!='Conserva de pescado') & 
                (df['codigo_partida']!='2301209000')) & (df['Sector']=='Pesquero'), 'grupo3'] = 'Otros prod. pesq.'

        # SECTOR2 - Agrupación amplia
        df['sector2'] = df['Sector']
        df.loc[(df['Sector']=='Siderúrgico') | (df['Sector']=='Metalúrgico'), 'sector2'] = 'Sidero-Metalúrgico'

        logger.info("Transformaciones completadas exitosamente")
        return df
    except Exception as e:
        logger.error(f"Error en transformaciones: {str(e)}")
        raise

