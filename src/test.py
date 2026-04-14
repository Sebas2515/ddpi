from transformations import aplicar_transformaciones
import pandas as pd

# =====================================
# CONFIGURACIÓN
# =====================================
SECTOR_TEST = 'Textil'   # 👉 usa None para ver todo

# =====================================
# DATA DE PRUEBA (VARIOS CASOS TEXTIL)
# =====================================
df_test = pd.DataFrame({
    'cod_pais': ['1','1','1','1'],
    'codigo_partida': ['6301300000','6301400000','6301500000','7407100000'],
    'cuatro_dig': ['6301','6301','6301','7407'],
    'fob': [1000000,2000000,1500000,3000000],
    'PesoNeto': [2000000,3000000,2500000,4000000],
    
    'Sector': ['Textil','Textil','Textil','Metalúrgico'],
    'Producto': ['Otras prendas','Otras prendas','Otras prendas','Barras y perfiles de cobre'],
    
    'Grupo': ['Test','Test','Test','Test'],
    
    # TEXTIL
    'Familia_Textil': ['Algodón','Lana','Sintético',''],
    'Material_Textil': ['Algodón','Lana y pelo fino','Sinteticas y artificiales',''],
    'Rubro_Textil': ['Prendas','Prendas','Prendas',''],
    
    # PESQUERO
    'Clasific_pesquero': ['','','',''],
    
    # OTROS
    'Industria_acero': ['','','',''],
    'cod_capitulo': ['63','63','63','74']
})

# =====================================
# TABLAS DUMMY
# =====================================
correlac_pais = pd.DataFrame({'cod_pais': ['1']})
correlac_prod = pd.DataFrame({'codigo_partida': [
    '6301300000','6301400000','6301500000','7407100000'
]})
correlac_cap = pd.DataFrame({'cuatro_dig': [
    '6301','7407'
]})

# =====================================
# EJECUTAR TRANSFORMACIONES
# =====================================
df = aplicar_transformaciones(
    df_test,
    correlac_pais,
    correlac_prod,
    correlac_cap
)

# =====================================
# DEBUG CLAVE (MUY IMPORTANTE)
# =====================================
print("\n=========== DEBUG PRODUCTOS ===========")
print(df[['Producto','Familia_Textil','Material_Textil','producto2','producto21']])

# =====================================
# FILTRO DINÁMICO
# =====================================
if SECTOR_TEST:
    df = df[df['Sector'] == SECTOR_TEST]
    print(f"\n=========== SECTOR: {SECTOR_TEST} ===========")

# =====================================
# DETALLE
# =====================================
print("\n--- DETALLE ---")
print(df[['Producto','Familia_Textil','producto2','producto21','fob']])

# =====================================
# VALIDACIÓN RÁPIDA
# =====================================
print("\n--- VALIDACIÓN producto2 ---")
print(df['producto2'].value_counts())

print("\n--- VALIDACIÓN producto21 ---")
print(df['producto21'].value_counts())

# =====================================
# RESUMEN TIPO TABLA DINÁMICA
# =====================================
print("\n--- RESUMEN (FOB por producto2) ---")
tabla = df.groupby(['producto2'])['fob'].sum().reset_index()
print(tabla)

# =====================================
# VALIDACIÓN TIPO EXCEL (CRUZADO)
# =====================================
print("\n--- TABLA CRUZADA ---")
pivot = pd.pivot_table(
    df,
    values='fob',
    index=['Producto','Familia_Textil'],
    columns='producto2',
    aggfunc='sum',
    fill_value=0
)
print(pivot)




from transformations import aplicar_transformaciones

import pandas as pd

df_test = pd.DataFrame({
    'cod_pais': ['1'],
    'codigo_partida': ['6301300000'],
    'cuatro_dig': ['6301'],
    'fob': [1000000],
    'PesoNeto': [2000000],
    'Sector': ['Textil'],
    'Producto': ['Otras prendas'],
    'Familia_Textil': ['Algodón'],
    'Material_Textil': [''],
    'Rubro_Textil': [''],
    'Clasific_pesquero': [''],
    'Industria_acero': [''],
    'cod_capitulo': ['63'],
    'Grupo': ['Test']
})

correlac_pais = pd.DataFrame({'cod_pais': ['1']})
correlac_prod = pd.DataFrame({'codigo_partida': ['6301300000']})
correlac_cap = pd.DataFrame({'cuatro_dig': ['6301']})

df = aplicar_transformaciones(df_test, correlac_pais, correlac_prod, correlac_cap)

print(df[['Producto','Familia_Textil','producto2']])