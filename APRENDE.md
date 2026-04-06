# 🎓 Guía de Aprendizaje del Proyecto RMC

## 1️⃣ COMENZAR AQUÍ: El Concepto General

### ¿Qué hace el proyecto?

Tu proyecto es un **pipeline de automatización** que:
1. **Lee** datos de exportaciones desde Excel
2. **Procesa** esos datos (agrupa, filtra, calcula)
3. **Transforma** los datos (agrega clasificaciones, enriquece con correlaciones)
4. **Crea tablas** pivote (resúmenes por sector, grupo, producto)
5. **Escribe en Excel** los resultados finales en una plantilla

### Analogía simple:

```
📥 Entrada          🔄 Procesamiento        📊 Análisis         📤 Salida
┌─────────┐         ┌────────────┐         ┌──────────┐        ┌─────────┐
│ Excel   │ ─────→ │ Limpiar &  │ ──────→ │ Crear   │ ─────→ │ Nuevo   │
│ datos   │        │ Agrupar    │        │ Tablas  │        │ Excel   │
└─────────┘        │ datos      │        │ resumen │        │ con     │
                   └────────────┘        │         │        │ reportes│
                                         └──────────┘        └─────────┘
```

---

## 2️⃣ Los 5 "Por Qué" Clave

### ¿Por qué hay 4 archivos diferentes?

```
BD_Expo (datos principales)
    ├─→ correlac_pais    (¿El código "051" es qué país?)
    ├─→ correlac_prod    (¿El código "0702" es qué producto?)
    └─→ correlac_cap     (¿A qué industria pertenece?)

Entonces construye la información completa:
  "051" ─→ Filipinas, ASIA
  "0702" ─→ Tomate, Agropecuario, Hortalizas
  "0702" ─→ Acero largo (si aplica)
```

### ¿Por qué se procesa en 3 pasos (base1, base2, data_final)?

```
Base1: Agrupa por variables clave
       └─ Suma el FOB y peso por partida/país/mes
       
Base2: Crea períodos especiales
       └─ "Ene 25", "Ult_12_meses" (últimos 12 meses)
       
Data_Final: Combine ambas
            └─ Tabla lista para transformar
```

### ¿Por qué hay producto2, grupo2, sector2?

Porque tu código original tiene **lógica compleja** de clasificación:

```
Caso 1: Si es Textil
  producto2 = Familia_Textil (en vez de nombre base)
  
Caso 2: Si es Zinc refinado
  producto2 = "Lingotes de zinc - JUMBO" (especial)
  
Caso 3: Si es Pesquero
  grupo2 = "Pescado", "Productos de anchoveta", etc.

Caso 4: Si es Textil AND Confecciones
  grupo2 = "Confecciones"
  grupo3 = "Textil-confecciones"
```

Es como tener **múltiples clasificaciones** según el contexto.

### ¿Por qué se guardan 3 archivos en data_loader?

Porque son **fuentes de verdad diferentes**:
- `correlac_pais.dta` → Viene de base de países global
- `correlac_prod.xlsx` → Viene de catálogo de productos
- `correlac_capitulo.dta` → Viene de clasificación industrial

Cada uno se **actualiza independientemente**.

### ¿Por qué se exporta a una plantilla Excel en vez de empezar de cero?

Porque:
- La plantilla tiene **formato fijo** (filas/columnas específicas)
- Tiene **fórmulas** que dependen de esos datos
- El reporte ya tiene **estructura definida** para cada hoja

Solo el pipeline **rellena los huecos**.

---

## 3️⃣ Flujo de Datos Paso a Paso

### PASO 1: Carga de Datos (data_loader.py)

```python
# Lee archivo Excel
bd = pd.read_excel("BD_Expo_2024-2026_ene.xlsx")
# Resultado: DataFrame con ~500,000 filas

# Lee correlacionadores
pais = pd.read_stata("correlac_2022_pais.dta")      # ~250 países
prod = pd.read_excel("correlac_2022_prod.xlsx")     # ~5,000 partidas
cap = pd.read_stata("correlac_2022_capitulo.dta")   # ~20 capítulos
```

### PASO 2: Procesamiento Inicial (processing.py)

```python
# 2.1 Renombrar columnas para consistencia
df.rename({'Subpartida': 'codigo_partida', ...})

# 2.2 Crear campos derivados
df['cod_capitulo'] = df['codigo_partida'].str[:2]   # Ej: "07"
df['cuatro_dig'] = df['codigo_partida'].str[:4]     # Ej: "0702"

# 2.3 PRIMERA AGREGACIÓN (suma por variables clave)
base1 = df.groupby(['cod_pais', 'codigo_partida', 'año', 'mes']).agg({
    'fob': 'sum',
    'PesoNeto': 'sum'
})
# Resultado: ~100,000 filas (más compacto)

# 2.4 Crear períodos especiales (últimos 12 meses)
base2 = crear_periodo_ultimos_12_meses(base1)

# 2.5 SEGUNDA AGREGACIÓN (combina períodos)
data_final = pd.concat([base1, base2]).groupby([...])
# Resultado: ~150,000 filas lista para transformar
```

**¿Por qué 2 agregaciones?** 
Porque necesitas datos TANTO por mes individual COMO por períodos acumulados.

### PASO 3: Transformaciones (transformations.py)

```python
# 3.1 Merge con correlacionadores
df = df.merge(correlac_pais)    # Agrega Pais, Pais_UE27
df = df.merge(correlac_prod)    # Agrega Producto, Sector, Grupo
df = df.merge(correlac_cap)     # Agrega Industria_acero

# 3.2 Crear variables monetarias
df['millones_fob'] = df['fob'] / 1_000_000      # Escala familiar
df['miles_TM'] = df['PesoNeto'] / 1_000_000

# 3.3 Aplicar lógica de clasificación (producto2, grupo2, etc)
# IF Sector == "Textil" THEN producto2 = Familia_Textil
# IF Producto == "Zinc refinado" THEN producto2 = "Lingotes zinc"
# ...etc (ver transformations.py para toda la lógica)

# Resultado: DataFrame enriquecido con ~30 columnas
```

### PASO 4: Generar Tablas (tables.py)

```python
# 4.1 Tabla Sectorial (nivel sector)
tabla_agro = df[df['sector2']=='Agropecuario'].pivot_table(
    index='sector2',           # Filas: sectores
    columns='periodo',         # Columnas: Ene25, Ene26, Ult12m
    values=['millones_fob', 'miles_TM'],
    aggfunc='sum'
)
# Resultado: 1 fila (Agropecuario), 6 columnas (FOB y TM × 3 períodos)

# 4.2 Tabla de Grupos
for grupo in ['Frutas', 'Hortalizas', ...]:
    tabla_grupo = tabla_pivote(grupo)
# Resultado: 15 grupos × 6 columnas cada uno

# 4.3 Ranking de Destinos (Top 5)
ranking = df.groupby('Pais_UE27')['millones_fob'].sum().sort_values()[-5:]
# Resultado: Top 5 países por FOB

# 4.4 Número de destinos
destinos = df.groupby('Pais')['Pais'].nunique()
# Resultado: ¿Cuántos países únicos por período?
```

### PASO 5: Exportar a Excel (excel_writer.py)

```python
# 5.1 Cargar plantilla base
wb = load_workbook("Cuadros de RMC-ene-2026.xlsx")

# 5.2 Escribir en hoja "Comercio_Agro"
hoja = wb['Comercio_Agro']
hoja.cell(10, 8).value = tabla_final.iloc[0, 0]  # Fila 10, Col H
hoja.cell(11, 8).value = tabla_final.iloc[1, 0]  # Fila 11, Col H
...

# 5.3 Escribir en hoja "comercio_Pesca"
hoja = wb['comercio_Pesca']
hoja.cell(10, 8).value = tabla_final.iloc[3, 0]
...

# 5.4 Guardar
wb.save("outputs/reportes/RMC_ene_2026.xlsx")
```

---

## 4️⃣ Estructura del Código

### Jerarquía de módulos:

```
main.py                 ← Punto de entrada
    ↓
pipeline.py            ← Orquestador (llama a todo en orden)
    ├─ data_loader.py       (Lee archivos)
    ├─ processing.py        (Procesa datos)
    ├─ transformations.py   (Transforma datos)
    ├─ tables.py            (Genera tablas)
    ├─ indices_generator.py (Genera índices)
    └─ excel_writer.py      (Escribe en Excel)

config.py              ← Variables globales
```

### Cada módulo es independiente:

```python
# En pipeline.py:
from src.data_loader import cargar_base
from src.processing import procesar_base
from src.transformations import aplicar_transformaciones

# Cada función:
# - Recibe un DataFrame
# - Lo modifica
# - Retorna el DataFrame modificado

df = cargar_base(config)              # INPUT: None, OUTPUT: df1
df = procesar_base(df, config)        # INPUT: df1, OUTPUT: df2
df = aplicar_transformaciones(df,...) # INPUT: df2, OUTPUT: df3
```

---

## 5️⃣ Variables Clave que Debes Conocer

### config.py:

```python
ANIOS = [2026, 2025]      # Años a procesar
MES_NUM = [1, 2]          # Hasta mes 1, elimina mes 2+
MES_ACTUAL = "ene"        # Nombre del mes

# Construye:
periodos = ["2025", "Ene 25", "Ene 26", "Ult_12_meses"]
```

### En processing.py:

```python
variables_a_agrupar_x = [
    'flujo_comercial',    # "EXPORTACION"
    'cod_pais',           # "051" (Filipinas)
    'cod_capitulo',       # "07" (productos vegetales)
    'codigo_partida',     # "0702000000" (tomate exacto)
    'año', 'mes',         # fecha
    'CADU', 'RUC'         # IDs
]
# Se agrupa POR estas variables y se suma FOB + Peso
```

### En transformations.py:

```python
# Se crean múltiples versiones de cada dimensión:
df['producto2']   # Producto con lógica especial
df['producto21']  # Producto con clasificación pesquera
df['producto3']   # Producto con familia textil

df['grupo2']      # Grupo principal
df['grupo3']      # Grupo detallado

df['sector2']     # Sector con Sidero-Metalúrgico agrupado
```

---

## 6️⃣ Ejemplo Concreto: Trazar 1 Registro

Imaginemos que entra este registro en BD_Expo:

```
Subpartida: 0702000000  (Tomate)
CPAIDES: 051            (¿Qué país?)
AÑO: 2026
MES: 1
VPESNET: 5000 kg
FOB: 12500 USD
```

### PASO 1: Carga
```
Lee directamente del Excel → Sin cambios aún
```

### PASO 2: Procesamiento
```
cod_capitulo = "07" (primeros 2 dígitos)
cuatro_dig = "0702" (primeros 4 dígitos)

PRIMERA AGREGACIÓN:
Se agrupa: flujo_comercial=EXPORTACION, cod_pais=051, 
           cod_capitulo=07, codigo_partida=0702000000, 
           año=2026, mes=1, CADU, RUC
           
Suma: fob=12500, PesoNeto=5000

SEGUNDA AGREGACIÓN (períodos):
Se asigna: periodo="Ene 26"
Se suma nuevamente con otros registros del mismo mes/año
```

### PASO 3: Transformaciones
```
Merge con correlac_pais:
  cod_pais=051 → Pais="Filipinas", Pais_UE27="ASIA"

Merge con correlac_prod:
  codigo_partida=0702000000 → 
    Producto="Tomate"
    Sector="Agropecuario"
    Grupo="Hortalizas"

Aplicar lógica:
  sector2 = "Agropecuario" (sin cambios)
  grupo2 = "Hortalizas" (sin cambios)
  producto2 = "Tomate" (sin cambios, no es caso especial)

Calcular monetarias:
  millones_fob = 12500 / 1000000 = 0.01245
  miles_TM = 5000 / 1000000 = 0.005
```

### PASO 4: Tablas
```
Se busca: ¿Hay filas con sector2="Agropecuario"?
Sí → Se incluye en tabla sectorial
   Filtra por periodo="Ene 26"
   Suma todos los FOB y pesos de Agro en Ene 26
   
Se busca: ¿Hay filas con grupo2="Hortalizas"?
Sí → Se incluye en tabla de grupos
   Suma todos los FOB y pesos de Hortalizas
   
Se busca: ¿Hay filas con Pais_UE27="ASIA"?
Sí → Se incluye en ranking de destinos
   Se ordena por FOB descendente
   Si está en Top 5 → Se escribe en Excel
```

### PASO 5: Excel
```
Encuentra: Comercio_Agro, Fila 10
Escribe: millones_fob = 0.01245 (entre otros)

Encuentra: Indices_X_Agro, Fila 11
Escribe: codigo_partida=0702000000, 
         miles_TM en columnas de períodos
```

---

## 7️⃣ Las 5 Preguntas Típicas

### P1: ¿Por qué se renombran las columnas?
**R:** Para consistencia. El Excel dice "Subpartida", pero en el código prefieres "codigo_partida" porque es más descriptivo.

### P2: ¿Qué es `fillna('NaN_temp')` y `replace`?
**R:** Pandas no suma bien si hay NaN. Usa un placebo ('NaN_temp'), suma, y luego repone los NaN.

```python
df['col'] = [1, NaN, 3]  # Problema
df['col'].fillna('NaN_temp')  # [1, 'NaN_temp', 3]
df.groupby(...).sum()  # Funciona
df['col'].replace('NaN_temp', NaN)  # [1, NaN, 3]
```

### P3: ¿Por qué se filtra por fecha?
**R:** Solo quieres datos hasta cierto mes. Ejemplo: "Enero 2026", así que eliminas Feb, Marzo, etc.

```python
base1 = base1[~((base1['año']==2026) & (base1['mes']>=2))]
# Significa: NO (año 2026 Y mes 2+)
```

### P4: ¿Qué hace `pivot_table`?
**R:** Transforma datos largos a anchos. Agrupación avanzada.

```
Entrada (largo):
Sector    Periodo  FOB
Agro      Ene25    10000
Agro      Ene26    15000
Pesca     Ene25    5000

Salida (ancho):
Sector    Ene25   Ene26
Agro      10000   15000
Pesca     5000    NaN
```

### P5: ¿Por qué escribir en una plantilla y no crear Excel de cero?
**R:** La plantilla tiene formato, fórmulas, gráficos. El pipeline solo llena datos.

---

## 8️⃣ MAPA DE APRENDIZAJE RECOMENDADO

### Semana 1: Conceptos
- [ ] Lee README.md (visión general)
- [ ] Lee REFERENCIA_RAPIDA.md (archivos que necesitas)
- [ ] Lee esta sección (1-3 arriba)

### Semana 2: Entrada y Salida
- [ ] Entiende qué van en data/raw/
- [ ] Entiende qué sale en outputs/
- [ ] Entiende la plantilla Excel

### Semana 3: El Flujo (en orden)
- [ ] Lee y entiende data_loader.py
- [ ] Lee y entiende processing.py
- [ ] Lee y entiende transformations.py
- [ ] Lee y entiende tables.py
- [ ] Lee y entiende excel_writer.py

### Semana 4: Lógica de Negocio
- [ ] Entiende config.py (qué se puede cambiar)
- [ ] Entiende la lógica de clasificación (producto2, grupo2, etc)
- [ ] Entiende cómo se generan períodos

### Semana 5: Casos de Uso
- [ ] Prueba cambiar un mes
- [ ] Prueba agregar una regla nueva en transformations.py
- [ ] Prueba modificar una fila en Excel manualmente

---

## 9️⃣ PREGUNTAR ESTRATÉGICAMENTE

Cuando preguntes, sé específico:

**❌ Malo:**
- "No entiendo la base de datos"

**✅ Bueno:**
- "En processing.py línea 25, ¿por qué se usa `fillna('NaN_temp')`? ¿No se puede usar 0?"

**❌ Malo:**
- "¿Cómo funciona el Excel?"

**✅ Bueno:**
- "En excel_writer.py, ¿por qué se escribe en fila 10 columna 8 en Comercio_Agro? ¿Cómo sé qué fila usar?"

---

## 🔟 EJERCICIOS PRÁCTICOS

### Ejercicio 1: Entender merge
```python
# En tu cabeza, predice qué pasa:
df = pd.DataFrame({'codigo': ['0702', '0703']})
corr = pd.DataFrame({'codigo': ['0702'], 'nombre': ['Tomate']})
resultado = df.merge(corr, on='codigo', how='left')

# ¿Cuántas filas tiene resultado?
# ¿Hay NaN en 'nombre'?
```

**Respuesta:** 2 filas. La fila "0703" tendrá NaN en 'nombre' porque no existe en correlacionador.

### Ejercicio 2: Entender groupby
```python
df = pd.DataFrame({
    'sector': ['Agro', 'Agro', 'Pesca'],
    'fob': [100, 200, 150]
})
resultado = df.groupby('sector')['fob'].sum()

# ¿Cuál es el resultado?
```

**Respuesta:**
```
sector
Agro     300
Pesca    150
```

### Ejercicio 3: Entender pivot_table
```python
df = pd.DataFrame({
    'sector': ['Agro', 'Agro', 'Pesca'],
    'periodo': ['Ene', 'Feb', 'Ene'],
    'fob': [100, 200, 150]
})
resultado = df.pivot_table(
    index='sector',
    columns='periodo',
    values='fob',
    aggfunc='sum'
)

# ¿Cuál es la forma (shape) del resultado?
```

**Respuesta:** (2, 2). 2 sectores, 2 períodos.

---

## 📞 Próximo Paso

Cuando estés listo:

1. Dime qué sección NO entiendes
2. Pregunta sobre un módulo específico (ej: "¿Qué hace data_loader.py línea X?")
3. Pregunta sobre un concepto (ej: "¿Por qué se usa merge y no vlookup?")
4. Pregunta sobre cambios (ej: "¿Cómo cambio la lógica de grupo2?")

**¿Por dónde quieres empezar?** 👇
