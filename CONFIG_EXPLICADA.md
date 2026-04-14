# ⚙️ Guía Completa de config.py

## 📍 Dónde Está

```
ddpi_rmc/
└─ src/
   └─ config.py  ← Este archivo
```

---

## 🎯 ¿Qué es config.py?

Es un archivo que **centraliza todas las variables que cambian**:
- Rutas de carpetas (dónde buscar archivos)
- Parámetros temporales (qué mes, qué año)
- Cálculo de períodos (períodos dinámicos)

**Ventaja:** En vez de buscar números en 10 archivos diferentes, cambias aquí UNA VEZ y se aplica a todo.

---

## 📖 Lectura Línea por Línea

### Línea 1-4: Docstring

```python
"""Configuración centralizada del proyecto.

Define rutas de entrada/salida, parámetros temporales y funciones de período.
"""
```

**Qué es:** Documentación del archivo (se ignora en ejecución, solo para humanos).

**Por qué importa:** Cuando alguien abre el archivo, entiende qué hace.

---

### Línea 6: Import

```python
from pathlib import Path
```

**Qué es:** Importa la librería `Path` de Python.

**Para qué:** Trabajar con rutas de carpetas de forma inteligente.

**Ejemplo:**
```python
# ❌ Malo (escrito manual):
ruta = "C:\Users\Sebasteitor\Desktop\..."

# ✅ Bueno (con Path):
ruta = Path("data") / "raw"  # Funciona en Windows y Linux
```

---

### Línea 8: BASE_DIR

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

**Desglose:**

| Parte | Qué hace |
|-------|----------|
| `__file__` | "Dónde está config.py" → `/Users/.../ddpi_rmc/src/config.py` |
| `.resolve()` | Convierte a ruta completa/absoluta |
| `.parent` | Sube una carpeta → `/Users/.../ddpi_rmc/src/` |
| `.parent` | Sube otra carpeta → `/Users/.../ddpi_rmc/` |

**Resultado:**
```
BASE_DIR = /Users/Sebasteitor/Desktop/DDPI_Repositorios/ddpi_rmc/
```

**Por qué:** Es el lugar "raíz" de donde TODO sale. Luego lo usamos para construir otras rutas.

**Cómo verificar:**
```python
# En Python, puedes hacer:
print(BASE_DIR)  # Verás la ruta exacta
```

---

### Líneas 10-12: Rutas de Entrada (Inputs)

```python
# 📥 Inputs
DATA_RAW = BASE_DIR / "data" / "raw"
TEMPLATES = BASE_DIR / "templates"
```

**Qué son:**

| Variable | Ruta | Qué va aquí |
|----------|------|-----------|
| `DATA_RAW` | `ddpi_rmc/data/raw/` | Los 4 archivos: BD_Expo, correlaciones |
| `TEMPLATES` | `ddpi_rmc/templates/` | Plantilla Excel (Cuadros de RMC-...) |

**Por qué "Inputs":** Son carpetas DONDE ENTRA información (lectura).

**Nota sobre /**

```python
BASE_DIR / "data" / "raw"
# Es lo mismo que:
Path("ddpi_rmc/data/raw")
# Es lo mismo que:
"ddpi_rmc\\data\\raw" en Windows
"ddpi_rmc/data/raw" en Linux/Mac
```

El `Path` es inteligente y se adapta al sistema operativo.

**Uso en código:**

```python
# En data_loader.py:
archivo = config.DATA_RAW / "BD_Expo_2024-2026_ene.xlsx"
# Resultado: /Users/.../ddpi_rmc/data/raw/BD_Expo_2024-2026_ene.xlsx

df = pd.read_excel(archivo)  # Lee el archivo
```

---

### Líneas 14-17: Rutas de Salida (Outputs)

```python
# 📤 Outputs
OUTPUTS = BASE_DIR / "outputs"
OUTPUT_TABLAS = OUTPUTS / "tablas"
OUTPUT_REPORTES = OUTPUTS / "reportes"
```

**Qué son:**

| Variable | Ruta | Qué va aquí |
|----------|------|-----------|
| `OUTPUTS` | `ddpi_rmc/outputs/` | Carpeta padre |
| `OUTPUT_TABLAS` | `ddpi_rmc/outputs/tablas/` | Tablas intermedias |
| `OUTPUT_REPORTES` | `ddpi_rmc/outputs/reportes/` | Excel final (RMC_ene_2026.xlsx) |

**Por qué "Outputs":** Son carpetas DONDE SALE información (escritura).

**Uso en código:**

```python
# En excel_writer.py:
output_file = config.OUTPUT_REPORTES / f"RMC_{mes}_{año}.xlsx"
# Resultado: /Users/.../ddpi_rmc/outputs/reportes/RMC_ene_2026.xlsx

wb.save(output_file)  # Guarda el archivo aquí
```

---

### Líneas 19-21: Parámetros Temporales

```python
# ⚙️ Parámetros
ANIOS = [2026, 2025]
MES_NUM = [2, 3]
MES_ACTUAL = "feb"
```

**Explicación detallada:**

#### `ANIOS = [2026, 2025]`

```
ANIOS[0] = 2026  ← Año ACTUAL (el que estás procesando)
ANIOS[1] = 2025  ← Año ANTERIOR (para comparar)
```

**Para qué sirve:**
- Procesa datos de 2025 Y 2026
- Filtra por "hasta 2026"
- Crea períodos como "Ene 25" vs "Ene 26"

**Cambio mensual:**
```python
# Enero 2026
ANIOS = [2026, 2025]  ← Sin cambio

# Enero 2027
ANIOS = [2027, 2026]  ← Cambiar si subes a 2027
```

#### `MES_NUM = [2, 3]`

**¿Qué significa?**

```
MES_NUM[0] = 2 ← Hasta febrero (inclusive)
MES_NUM[1] = 3 ← Elimina marzo en adelante
```

**En código (processing.py):**
```python
# Filtra así:
base = base[~((base['año']==2026) & (base['mes']>=3))]
# "NO (año 2026 Y mes 3+)"
# Resultado: Mantiene enero-febrero, elimina marzo-diciembre
```

**Por qué:** Si estás en febrero, solo quieres datos hasta febrero, no datos futuros de marzo.

**Mapeo de meses:**
```
1 = Enero
2 = Febrero
3 = Marzo
4 = Abril
...
12 = Diciembre
```

**Cambio mensual:**
```python
# Enero (hasta enero, elimina febrero)
MES_NUM = [1, 2]

# Febrero (hasta febrero, elimina marzo)
MES_NUM = [2, 3]  ← Estamos aquí ahora

# Marzo (hasta marzo, elimina abril)
MES_NUM = [3, 4]

# Diciembre (hasta diciembre, elimina enero del próximo año)
MES_NUM = [12, 1]
```

#### `MES_ACTUAL = "feb"`

**Qué es:** Nombre del mes para construir nombres de archivo.

**Uso:**
```python
# En excel_writer.py:
archivo_plantilla = f"Cuadros de RMC-{MES_ACTUAL}-{ANIOS[0]}-Joel-act.xlsx"
# Resultado: "Cuadros de RMC-feb-2026-Joel-act.xlsx"

archivo_salida = f"RMC_{MES_ACTUAL}_{ANIOS[0]}.xlsx"
# Resultado: "RMC_feb_2026.xlsx"
```

**Cambio mensual:**
```python
# Cambiar solo MES_ACTUAL:
MES_ACTUAL = "ene"   # Enero
MES_ACTUAL = "feb"   # Febrero
MES_ACTUAL = "mar"   # Marzo
...
MES_ACTUAL = "dic"   # Diciembre
```

---

### Líneas 23-48: Función construir_periodos()

```python
def construir_periodos():
    """Construye dinámicamente los periodos según el mes actual.
    
    Returns:
        tuple: (periodo_crear, periodos)
    """
    if MES_ACTUAL == "ene":
        periodo_crear = [
            f"Ene {str(ANIOS[0]-1)[-2:]}",
            f"Ene {str(ANIOS[0])[-2:]}",
            "Ult_12_meses"
        ]
    else:
        periodo_crear = [
            f"Ene-{MES_ACTUAL} {str(ANIOS[0]-1)[-2:]}",
            f"Ene-{MES_ACTUAL} {str(ANIOS[0])[-2:]}",
            "Ult_12_meses"
        ]

    periodos = [str(ANIOS[1]), periodo_crear[0], periodo_crear[1], periodo_crear[2]]
    return periodo_crear, periodos
```

**¿Qué hace?** Construye DINÁMICAMENTE los períodos según el mes.

**Caso 1: Si MES_ACTUAL = "ene"**

```python
ANIOS[0] = 2026
ANIOS[0]-1 = 2025

str(ANIOS[0]-1)[-2:] = "25" (últimos 2 dígitos de 2025)
str(ANIOS[0])[-2:] = "26" (últimos 2 dígitos de 2026)

periodo_crear = [
    "Ene 25",       # Enero del año anterior
    "Ene 26",       # Enero del año actual
    "Ult_12_meses"  # Últimos 12 meses completos
]

periodos = [
    "2025",         # Año anterior completo
    "Ene 25",       # Del período anterior
    "Ene 26",       # Del período actual
    "Ult_12_meses"  # Últimos 12 meses
]
```

**Caso 2: Si MES_ACTUAL = "feb"** (AQUÍ ESTAMOS AHORA)

```python
periodo_crear = [
    f"Ene-feb {str(2025)[-2:]}" = "Ene-feb 25",    # Enero-Febrero 2025
    f"Ene-feb {str(2026)[-2:]}" = "Ene-feb 26",    # Enero-Febrero 2026
    "Ult_12_meses"                                  # Últimos 12 meses
]

periodos = [
    "2025",         # Año anterior completo
    "Ene-feb 25",
    "Ene-feb 26",
    "Ult_12_meses"
]
```

**¿Por qué IF/ELSE?** 
Porque enero es especial: solo hay un mes, así que pone "Ene".
Otros meses: incluye rango "Ene-Feb", "Ene-Mar", etc.

**Cómo se usa en pipeline:**
```python
periodo_crear, periodos = config.construir_periodos()

# Ahora accedes a:
periodo_crear[0]   = "Ene-feb 25"
periodo_crear[1]   = "Ene-feb 26"
periodo_crear[2]   = "Ult_12_meses"

periodos = ["2025", "Ene-feb 25", "Ene-feb 26", "Ult_12_meses"]
```

---

## 🔄 Flujo Completo: Cómo CONFIG Afecta TODO

```
1. DEFINES en config.py:
   MES_ACTUAL = "feb"
   ANIOS = [2026, 2025]
   MES_NUM = [2, 3]

2. En data_loader.py:
   archivo = DATA_RAW / f"BD_Expo_{ANIOS[0]-2}-{ANIOS[0]}_{MES_ACTUAL}.xlsx"
   # = "BD_Expo_2024-2026_feb.xlsx"  ← Lee este archivo

3. En processing.py:
   # Filtra por MES_NUM:
   base = base[~((base['año']==ANIOS[0]) & (base['mes']>=MES_NUM[1]))]
   # Elimina marzo en adelante

4. En pipeline.py:
   periodo_crear, periodos = config.construir_periodos()
   # = (["Ene-feb 25", "Ene-feb 26", "Ult_12_meses"], [...])

5. En excel_writer.py:
   wb = load_workbook(TEMPLATES / f"Cuadros de RMC-{MES_ACTUAL}-{ANIOS[0]}-...")
   # = "Cuadros de RMC-feb-2026-..."
   
   output = OUTPUT_REPORTES / f"RMC_{MES_ACTUAL}_{ANIOS[0]}.xlsx"
   # = "RMC_feb_2026.xlsx"  ← Guarda aquí
```

---

## 📋 TABLA DE CAMBIOS MENSUALES

Cuando cambies de mes, modifica ESTOS VALORES en config.py:

| Cambio | Enero | Febrero | Marzo | ... | Diciembre |
|--------|-------|---------|-------|-----|-----------|
| `MES_ACTUAL` | `"ene"` | `"feb"` | `"mar"` | ... | `"dic"` |
| `MES_NUM[0]` | `1` | `2` | `3` | ... | `12` |
| `MES_NUM[1]` | `2` | `3` | `4` | ... | `1` |
| `ANIOS[0]` | `2026` | `2026` | `2026` | ... | `2026` |
| `ANIOS[1]` (si sube año) | `2025` | `2025` | `2025` | ... | `2025` → `2026` |

**Nota:** Si pasas a Enero 2027, cambia ambos ANIOS:
```python
# Diciembre 2026
ANIOS = [2026, 2025]

# Enero 2027
ANIOS = [2027, 2026]  ← Ambos suben 1
```

---

## ⚠️ Errores Comunes

### Error 1: Cambiar solo MES_ACTUAL
```python
# ❌ MALO:
MES_ACTUAL = "mar"
# Pero MES_NUM sigue siendo [2, 3] = Febrero-Marzo

# ✅ BUENO:
MES_ACTUAL = "mar"
MES_NUM = [3, 4]  ← También cambiar esto
```

### Error 2: Olvidar que MES_NUM [1] es EXCLUSIVO
```python
# Si MES_NUM = [2, 3]
# Procesa HASTA mes 2 (febrero)
# ELIMINA mes 3 EN ADELANTE (marzo+)

# NO procesa:
# - Mes 1 (enero)  ← ¡PERDISTE ENERO!

# ✅ CORRECTO:
# Para procesar SOLO febrero:
# Deberías haber puesto MES_NUM = [2, 3]  ← Correcto
```

### Error 3: Nombres de archivo inconsistentes
```python
# Si MES_ACTUAL = "feb" pero tu archivo es:
# BD_Expo_2024-2026_ene.xlsx  ← Enero, no febrero
# 
# El script buscará:
# BD_Expo_2024-2026_feb.xlsx  ← Febrero
# 
# ❌ NO ENCONTRARÁ el archivo
```

---

## 🎯 RESUMEN RÁPIDO

### Para entender config.py:

```
┌─ BASE_DIR ────────────────────┐
│ Encuentra la carpeta raíz      │
│ Ejemplo: "ddpi_rmc/"           │
└────────────────────────────────┘

┌─ RUTAS ────────────────────────┐
│ DATA_RAW ← Dónde enteran datos  │
│ TEMPLATES ← Dónde entra plantilla
│ OUTPUTS ← Dónde SALEN resultados
└────────────────────────────────┘

┌─ PARÁMETROS ───────────────────┐
│ ANIOS ← Qué años procesar      │
│ MES_NUM ← Hasta qué mes        │
│ MES_ACTUAL ← Nombre del mes    │
└────────────────────────────────┘

┌─ FUNCIÓN ──────────────────────┐
│ construir_periodos()           │
│ → Crea listados dinámicos      │
│   según mes actual             │
└────────────────────────────────┘
```

---

## 💡 EJERCICIO PRÁCTICO

### Pregunta 1: ¿Qué ruta es DATA_RAW?

```python
BASE_DIR = "/Users/Sebasteitor/Desktop/DDPI_Repositorios/ddpi_rmc"
DATA_RAW = BASE_DIR / "data" / "raw"

# ¿Cuál es DATA_RAW?
```

**Respuesta:** `/Users/Sebasteitor/Desktop/DDPI_Repositorios/ddpi_rmc/data/raw`

### Pregunta 2: ¿Cuál será el nombre del archivo de salida?

```python
MES_ACTUAL = "feb"
ANIOS = [2026, 2025]

# En excel_writer.py:
archivo = f"RMC_{MES_ACTUAL}_{ANIOS[0]}.xlsx"

# ¿Cuál es el nombre?
```

**Respuesta:** `RMC_feb_2026.xlsx`

### Pregunta 3: ¿Qué archivos sé que busca?

```python
MES_ACTUAL = "mar"
ANIOS = [2026, 2025]

# En data_loader.py busca:
f"BD_Expo_{ANIOS[0]-2}-{ANIOS[0]}_{MES_ACTUAL}.xlsx"

# ¿Cuál es el nombre?
```

**Respuesta:** `BD_Expo_2024-2026_mar.xlsx`

---

## 🚀 Próximo Paso

Cuando entiendas config.py:

1. Intenta cambiar `MES_ACTUAL` a "mar" y ajusta `MES_NUM`
2. Verifica que los archivos que busca existan con esos nombres
3. Pregunta: "¿Cómo sé que config.py se está usando correctamente?"

**¿Tienes dudas sobre alguna línea específica?** 👇

---

---

# 📂 data_loader.py - Cargador de Datos

## 📍 Ubicación

```
ddpi_rmc/
└─ src/
   └─ data_loader.py  ← Este archivo
```

---

## 🎯 ¿Qué es data_loader.py?

Es el **guardia de la entrada**: 
- Verifica que los archivos existan
- Lee archivos Excel (extensión .xlsx)
- Lee archivos Stata (extensión .dta)
- Si algo está mal, **detiene todo y avisa**

**Analogía:**
```
config.py       → Dice QUÉ archivos buscar
data_loader.py  → Los BUSCA y LOS LEE
```

---

## 📖 Lectura Línea por Línea

### Líneas 1-4: Imports (Librerías)

```python
import pandas as pd
import logging
from pathlib import Path
```

**Qué son:**

| Librería | Para qué | Símbolo |
|----------|----------|--------|
| `pandas` | Leer/procesar datos en tablas | `pd` |
| `logging` | Registrar eventos (info, errores) | `logging` |
| `pathlib` | Trabajar con rutas de carpetas | `Path` |

**Ejemplo de uso:**
```python
import pandas as pd
df = pd.read_excel("mi_archivo.xlsx")  # Lee Excel

import logging
logger = logging.getLogger(__name__)
logger.info("El archivo se cargó")  # Escribe en log

from pathlib import Path
ruta = Path("data") / "raw"  # Construye rutas inteligentes
```

---

### Línea 5: Logger

```python
logger = logging.getLogger(__name__)
```

**Qué hace:**
- Crea un "registro" para este archivo
- `__name__` = nombre del módulo ("data_loader")

**Qué es un logger:**
```
"El 3 de abril 2026, 14:30:45 - data_loader.py: Cargando archivo BD_Expo..."
 └─────────────┬──────────────┘  └────┬───────┘  └──────────────┬──────────────┘
               fecha/hora             módulo                     mensaje
```

**Tipos de mensajes:**
```python
logger.info("Mensaje de información")      # Azul, todo OK
logger.warning("Advertencia")              # Amarillo, posible problema
logger.error("Error ocurrió")              # Rojo, algo falló
logger.debug("Detalles técnicos")          # Gris, solo si debugging
```

---

### Línea 7: Función cargar_base(config)

```python
def cargar_base(config):
    """Carga la base de datos desde archivo Excel con validación."""
```

**Qué recibe:** El objeto `config` (que contiene DATA_RAW, MES_ACTUAL, etc.)

**Qué devuelve:** Un DataFrame de pandas con todos los datos

**¿Cuándo se llama?**
```python
# En pipeline.py:
from src import data_loader
base = data_loader.cargar_base(config)  # Se llama aquí
```

---

### Línea 8-9: Lista de Columnas String

```python
try:
    columnas_str = ['Subpartida', '2 digitos', 'CADU', 'RUC', 'CVIATRA', '4 digitos']
```

**¿Qué es columnas_str?**

Lista de nombres de columnas que deben tratarse como **texto**, NO como números.

**¿Por qué es importante?**

| Tipo | Problema | Ejemplo |
|------|----------|---------|
| ❌ Número | Pierde ceros al principio | `"0012345"` → `12345` |
| ✅ Texto | Mantiene todo igual | `"0012345"` → `"0012345"` |

**Ejemplo real:**
```python
# RUC de Perú: "20123456789"
# Si lo tratas como número: 20123456789
# Si lo tratas como texto: "20123456789"

# El código de aduanas: "0101010101"
# Si es número: 101010101 (¡perdiste los ceros!)
# Si es texto: "0101010101" (correcto)
```

---

### Línea 11-12: Construir Ruta del Archivo

```python
file = config.DATA_RAW / f"BD_Expo_{config.ANIOS[0]-2}-{config.ANIOS[0]}_{config.MES_ACTUAL}.xlsx"
```

**Desglose:**

```
config.DATA_RAW                    = "/Users/.../ddpi_rmc/data/raw/"
config.ANIOS[0]                    = 2026
config.ANIOS[0]-2                  = 2024
config.MES_ACTUAL                  = "feb"

f"BD_Expo_{config.ANIOS[0]-2}-{config.ANIOS[0]}_{config.MES_ACTUAL}.xlsx"
= f"BD_Expo_2024-2026_feb.xlsx"

file = "/Users/.../ddpi_rmc/data/raw/BD_Expo_2024-2026_feb.xlsx"
```

**¿Por qué ANIOS[0]-2?**

| Año Actual | -2 | Rango |
|------------|-----|-------|
| 2026 | 2024 | 2024-2026 (últimos 3 años) |
| 2027 | 2025 | 2025-2027 (últimos 3 años) |

Es **dinámico**: cambias `ANIOS[0]` en config.py y automáticamente busca el rango correcto.

---

### Línea 14-15: Verificación de Existencia

```python
if not file.exists():
    raise FileNotFoundError(f"Archivo no encontrado: {file}")
```

**Qué hace:**
1. `file.exists()` → ¿El archivo existe? Sí/No
2. `not` → Invierte la respuesta
3. `if not file.exists()` → Si el archivo NO existe...
4. `raise FileNotFoundError()` → **DETÉN TODO y muestra error**

**Ejemplo:**

```python
# Caso 1: Archivo EXISTE
file = "/Users/.../data/raw/BD_Expo_2024-2026_feb.xlsx"
file.exists() = True
not True = False
if False:  # No entra aquí
    raise...

# Resultado: Continúa normal ✅


# Caso 2: Archivo NO existe
file = "/Users/.../data/raw/BD_Expo_2024-2026_mar.xlsx"  # ← ¡NO EXISTE!
file.exists() = False
not False = True
if True:  # ¡Entra aquí!
    raise FileNotFoundError(...)
    
# Resultado: Se detiene y muestra:
# FileNotFoundError: Archivo no encontrado: /Users/.../BD_Expo_2024-2026_mar.xlsx
```

**¿Por qué?** Mejor **fallar rápido** que procesar datos fantasma.

---

### Línea 17-18: Logger y read_excel

```python
logger.info(f"Cargando archivo: {file}")
df = pd.read_excel(
```

**Línea 17:**
```python
logger.info(f"Cargando archivo: {file}")
```
Registra: `"data_loader.py: Cargando archivo: /Users/.../BD_Expo_2024-2026_feb.xlsx"`

**Línea 18:** Empieza a leer el archivo con `pd.read_excel()` (continúa...)

---

### Líneas 18-22: Parámetros de read_excel

```python
df = pd.read_excel(
    file,                                    # ← Qué archivo leer
    keep_default_na=False,                   # ← Opción 1
    dtype={col: 'str' for col in columnas_str}  # ← Opción 2
)
```

**Parámetro 1: `file`**
```python
file = "/Users/.../BD_Expo_2024-2026_feb.xlsx"
# Lee este archivo específico
```

**Parámetro 2: `keep_default_na=False`**

```
keep_default_na = Mantener valores NA (faltantes) como texto

Ejemplo en Excel:
┌─────────────┬──────────┐
│ RUC         │ Valor    │
├─────────────┼──────────┤
│ 20123456789 │ NA       │
│ 20987654321 │ 1500     │
└─────────────┴──────────┘

Con keep_default_na=True (MALO):
- "NA" en Excel → NaN en Python (faltante)

Con keep_default_na=False (BUENO):
- "NA" en Excel → "NA" en Python (texto literal)
```

**¿Por qué?** Porque puede haber datos que literalmente digan "NA" y no queremos perderlos.

**Parámetro 3: `dtype={...}`**

```python
dtype={col: 'str' for col in columnas_str}
```

**Desglose:**
```python
columnas_str = ['Subpartida', '2 digitos', 'CADU', 'RUC', 'CVIATRA', '4 digitos']

# Crea un diccionario:
{
    'Subpartida': 'str',
    '2 digitos': 'str',
    'CADU': 'str',
    'RUC': 'str',
    'CVIATRA': 'str',
    '4 digitos': 'str'
}

# Le dice a pandas: "Trata TODAS estas columnas como texto"
```

**Resultado:**
```python
df['RUC'] = ['20123456789', '20987654321', '20555555555']  # Texto
# NO:
df['RUC'] = [20123456789, 20987654321, 20555555555]       # Números ❌
```

---

### Línea 24: Log de Éxito

```python
logger.info(f"Base cargada con éxito: {len(df)} registros")
```

**Qué dice:**
```
"data_loader.py: Base cargada con éxito: 45230 registros"
```

`len(df)` = cantidad de filas en el DataFrame.

**Ejemplo:**
```python
df:
┌─────┬────────┐
│ RUC │ Valor  │
├─────┼────────┤
│ 123 │ 1500   │
│ 456 │ 2000   │
│ 789 │ 3500   │
└─────┴────────┘

len(df) = 3
```

---

### Línea 26: Retorno

```python
return df
```

**Qué devuelve:** El DataFrame completo con todos los datos cargados.

**Quién lo recibe:**
```python
# En pipeline.py:
base = data_loader.cargar_base(config)
# base = el DataFrame devuelto
```

---

### Líneas 27-30: Manejo de Errores

```python
except FileNotFoundError as e:
    logger.error(str(e))
    raise
except Exception as e:
    logger.error(f"Error al cargar base: {str(e)}")
    raise
```

**Qué es try/except:**

```python
try:
    # Intenta esto
    hacer_algo_peligroso()
except ErrorTipo1:
    # Si falla con ErrorTipo1, haz esto
    mostrar_mensaje()
except ErrorTipo2:
    # Si falla con ErrorTipo2, haz esto otro
    mostrar_otro_mensaje()
```

**En nuestro caso:**

```python
try:
    # Intenta cargar el archivo
    df = pd.read_excel(file, ...)
except FileNotFoundError as e:
    # Si FILE NOT FOUND (el archivo no existe)
    logger.error(str(e))        # Registra el error
    raise                        # Re-lanza el error (detiene todo)
except Exception as e:
    # Si CUALQUIER OTRO ERROR ocurre
    logger.error(f"Error al cargar base: {str(e)}")
    raise
```

**Ejemplo de flujo:**

```
┌─────────────────────────────┐
│ try:                        │
│   df = read_excel(file)     │
│                             │
│ except FileNotFoundError:   │
│   → Si archivo NO existe    │
│     logger.error(...)       │
│     raise                   │
│                             │
│ except Exception:           │
│   → Si OTRO error          │
│     logger.error(...)       │
│     raise                   │
└─────────────────────────────┘

Si TODO va bien:
→ Continúa a return df ✅

Si algo falla:
→ Se detiene y muestra error ❌
```

---

## 📥 Función cargar_correlaciones(config)

### Línea 34: Definición

```python
def cargar_correlaciones(config):
    """Carga archivos de correlaciones con validación."""
```

**Qué es:** Carga 3 archivos DIFERENTES de correlaciones (no solo 1 como cargar_base).

**Por qué 3 archivos:**
- Uno para países (pais.dta)
- Uno para productos (prod.xlsx)
- Uno para capítulos (capitulo.dta)

**¿Cuándo se llama?**
```python
# En pipeline.py:
correlac_pais, correlac_prod, correlac_cap = data_loader.cargar_correlaciones(config)
```

---

### Línea 37: Logger

```python
logger.info("Cargando correlaciones...")
```

Registra que comenzó el proceso.

---

### Líneas 39-41: Rutas de los 3 Archivos

```python
archivo_pais = config.DATA_RAW / "correlac_2022_pais.dta"
archivo_prod = config.DATA_RAW / "correlac_2022_prod.xlsx"
archivo_cap = config.DATA_RAW / "correlac_2022_capitulo.dta"
```

**¿Dónde están?**

Todos en la carpeta `config.DATA_RAW` que vimos en config.py:

```
ddpi_rmc/data/raw/
├─ BD_Expo_2024-2026_feb.xlsx
├─ correlac_2022_pais.dta           ← Aquí
├─ correlac_2022_prod.xlsx          ← Aquí
└─ correlac_2022_capitulo.dta       ← Aquí
```

**¿Qué es .dta?**

Formato de archivo de Stata (software estadístico). Similar a Excel pero para datos estadísticos.

| Formato | Uso | Leído con |
|---------|-----|-----------|
| .xlsx | Excel (hojas, celdas) | `pd.read_excel()` |
| .dta | Stata (datos estadísticos) | `pd.read_stata()` |
| .csv | Texto separado por comas | `pd.read_csv()` |

---

### Líneas 43-45: Validación de Existencia

```python
for archivo in [archivo_pais, archivo_prod, archivo_cap]:
    if not archivo.exists():
        raise FileNotFoundError(f"Archivo faltante: {archivo}")
```

**Qué hace:**
1. Crea una lista: `[archivo_pais, archivo_prod, archivo_cap]`
2. Para CADA archivo en la lista:
3. Si NO existe → DETÉN TODO

**Equivalente sin loop:**
```python
# ❌ REPETITIVO:
if not archivo_pais.exists():
    raise FileNotFoundError(...)
if not archivo_prod.exists():
    raise FileNotFoundError(...)
if not archivo_cap.exists():
    raise FileNotFoundError(...)

# ✅ CON LOOP (lo que hace):
for archivo in [archivo_pais, archivo_prod, archivo_cap]:
    if not archivo.exists():
        raise FileNotFoundError(...)
```

**¿Por qué?** Menos código, más elegante.

---

### Líneas 47-49: Lectura de Archivos

```python
correlac_pais = pd.read_stata(archivo_pais)
correlac_prod = pd.read_excel(archivo_prod)
correlac_cap = pd.read_stata(archivo_cap)
```

**Lectura según formato:**

| Variable | Archivo | Formato | Función |
|----------|---------|---------|---------|
| `correlac_pais` | `pais.dta` | Stata (.dta) | `read_stata()` |
| `correlac_prod` | `prod.xlsx` | Excel (.xlsx) | `read_excel()` |
| `correlac_cap` | `capitulo.dta` | Stata (.dta) | `read_stata()` |

**Resultado:** 3 DataFrames cargados.

---

### Línea 51: Log de Éxito

```python
logger.info(f"Correlaciones cargadas exitosamente")
```

Registra que todo salió bien.

---

### Línea 52: Retorno

```python
return correlac_pais, correlac_prod, correlac_cap
```

**Devuelve:** Los 3 DataFrames como tupla.

**Quién lo recibe:**
```python
# En pipeline.py:
correlac_pais, correlac_prod, correlac_cap = data_loader.cargar_correlaciones(config)
# Aquí se "desempaquetan" los 3 valores
```

**¿Qué es tupla?**

```python
# Tupla = Lista inmutable de valores
tupla = (100, 200, 300)

# Desempaquetar:
a, b, c = tupla
# a = 100
# b = 200
# c = 300
```

---

### Líneas 53-55: Manejo de Errores

```python
except Exception as e:
    logger.error(f"Error cargando correlaciones: {str(e)}")
    raise
```

Si CUALQUIER error ocurre:
1. Registra el error
2. Detiene todo

---

## 🔄 Flujo Completo de data_loader.py

```
┌──────────────────────────────────────────┐
│ pipeline.py llama:                       │
│ base = cargar_base(config)               │
│ correlac_p, correlac_pr, correlac_c =    │
│    cargar_correlaciones(config)          │
└──────────────────────────────────────────┘

        ↓ ENTRA A data_loader.py ↓

┌──────── cargar_base() ────────┐
│ 1. Lee config.ANIOS, .MES_ACT │
│ 2. Construye ruta del archivo │
│ 3. Valida que exista          │
│ 4. Lee con pd.read_excel()    │
│    - keep_default_na=False    │
│    - dtype como texto         │
│ 5. Registra éxito             │
│ 6. Devuelve DataFrame         │
└───────────────────────────────┘

        ↓

┌── cargar_correlaciones() ──┐
│ 1. Construye 3 rutas       │
│ 2. Valida que existan      │
│ 3. Lee con:                │
│    - read_stata() para .dta │
│    - read_excel() para .xlsx│
│ 4. Registra éxito          │
│ 5. Devuelve 3 DataFrames   │
└────────────────────────────┘

        ↓ VUELVEN A pipeline.py ↓

base = DataFrame con 45,230 registros
correlac_pais = DataFrame con países
correlac_prod = DataFrame con productos
correlac_cap = DataFrame con capítulos
```

---

## 📋 TABLA RÁPIDA

| Función | Qué Lee | Validación | Retorna |
|---------|---------|-----------|---------|
| `cargar_base()` | BD_Expo_2024-2026_feb.xlsx | ✅ Existe | 1 DataFrame |
| `cargar_correlaciones()` | pais.dta, prod.xlsx, capitulo.dta | ✅ Existen 3 | 3 DataFrames |

---

## ⚠️ Errores Comunes

### Error 1: Archivo NO existe

```python
# Si config.MES_ACTUAL = "mar" pero no tienes:
# BD_Expo_2024-2026_mar.xlsx

# data_loader.py busca:
# BD_Expo_2024-2026_mar.xlsx  ← ¡NO EXISTE!

# Resultado:
FileNotFoundError: Archivo no encontrado: /Users/.../BD_Expo_2024-2026_mar.xlsx

# Solución:
1. Verifica que el archivo EXISTA en data/raw/
2. O cambia config.MES_ACTUAL al mes correcto
```

### Error 2: Columnas con ceros perdidos

```python
# ❌ SIN especificar dtype:
df['RUC'] = [20123456789, 20987654321]  # ¡Números!

# ✅ CON dtype='str':
df['RUC'] = ['20123456789', '20987654321']  # ¡Texto!
```

### Error 3: Falta un archivo de correlación

```python
# Si no tienes: correlac_2022_prod.xlsx

# data_loader.py busca:
# correlac_2022_pais.dta       ✅ OK
# correlac_2022_prod.xlsx      ❌ FALTA
# correlac_2022_capitulo.dta   ✅ OK

# Resultado:
FileNotFoundError: Archivo faltante: /Users/.../correlac_2022_prod.xlsx

# El script se detiene aunque 2 de 3 existan
```

---

## 🎯 RESUMEN

data_loader.py es el **guardia de entrada**:

```
✅ Valida que archivos existan
✅ Lee archivos Excel (.xlsx) y Stata (.dta)
✅ Trata ciertos campos como TEXTO (no números)
✅ Registra todo en logs
❌ Si algo está mal, DETIENE TODO
```

**Conexión con config.py:**
- config.DATA_RAW → Dónde buscar archivos
- config.ANIOS[0] → Rango de años en nombre
- config.MES_ACTUAL → Qué mes en nombre
- config.ANIOS[0]-2 → Años previos automáticos

---

## 💡 EJERCICIOS

### Pregunta 1: ¿Qué archivo busca cargar_base()?

```python
# config.py tiene:
config.ANIOS = [2026, 2025]
config.MES_ACTUAL = "mar"
config.DATA_RAW = "/Users/.../ddpi_rmc/data/raw"

# ¿Cuál es la ruta completa?
```

**Respuesta:** `/Users/.../ddpi_rmc/data/raw/BD_Expo_2024-2026_mar.xlsx`

### Pregunta 2: ¿Por qué ANIOS[0]-2 y no ANIOS[0]?

```python
# Si ANIOS[0] = 2026:
# Con -2:     2024-2026 (3 años)
# Sin -2:     2026-2026 (1 año)

# ¿Cuál es más útil?
```

**Respuesta:** Con -2. Tienes los últimos 3 años complete para análisis.

### Pregunta 3: ¿Qué diferencia hay entre read_excel() y read_stata()?

```python
# read_excel() → Formato .xlsx (Excel)
# read_stata() → Formato .dta (Stata)

# Ambos devuelven what?
```

**Respuesta:** Ambos devuelven un DataFrame de pandas. Solo cambia el formato de entrada.

---

---

# 🔄 processing.py - Procesamiento (Las 3 Agregaciones)

## 📍 Ubicación

```
ddpi_rmc/
└─ src/
   └─ processing.py  ← Este archivo
```

---

## 🎯 ¿Qué es processing.py?

Es el **corazón de la lógica**: 

- **Renombra columnas** de nombres extraños a nombres amigables
- **Crea campos derivados** (capítulo, 4 dígitos)
- **Hace 3 agregaciones** (groupby) sucesivas
- **Filtra por mes actual** (elimina datos futuros)
- **Construye períodos dinámicos** (años, acumulados)

**Analogía:**
```
data_loader.py  → Trae datos brutos (caótico)
processing.py   → Los LIMPIA, ORGANIZA y AGRUPA (orden perfecto)
```

**¿Por qué 3 agregaciones?**

Porque necesitas datos en 3 niveles:
1. **Nivel detalle** (base1_x): Cada país, cada producto, cada mes
2. **Nivel período acumulado** (base2_x): Enero-Febrero completo
3. **Nivel final** (data_final_x): Todo consolidado por períodos

---

## 📖 Lectura Línea por Línea

### Líneas 1-5: Imports y Logger

```python
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)
```

**Qué importa:**

| Librería | Símbolo | Para qué |
|----------|---------|----------|
| pandas | `pd` | Leer/procesar DataFrames |
| numpy | `np` | Operaciones numéricas avanzadas (aquí: np.nan) |
| logging | `logging` | Registrar eventos |

**Logger:** Igual que en data_loader.py.

---

### Línea 7: Función procesar_base(df, config)

```python
def procesar_base(df, config):
    """Procesa la base de datos: renombra columnas, crea campos derivados, agrupa y expande periodos."""
```

**Qué recibe:**
- `df` → DataFrame del data_loader (45,000 registros con columnas raras)
- `config` → Objeto de configuración (ANIOS, MES_NUM, etc.)

**Qué devuelve:**
- `data_final_x` → DataFrame procesado (agrupado 3 veces, con períodos)

**¿Cuándo se llama?**
```python
# En pipeline.py:
base = data_loader.cargar_base(config)
data_final = processing.procesar_base(base, config)
```

---

### Línea 11: Try/Except

```python
try:
    logger.info(f"Iniciando procesamiento de {len(df)} registros")
```

Comienza con validación: "¿Se recibieron datos?"

---

## 🔤 PARTE 1: RENOMBRAR COLUMNAS

### Líneas 14-21: Rename (Renombrar)

```python
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
```

**¿Por qué renombrar?**

Las columnas originales tienen nombres raros de aduanas:
- `Subpartida` → `codigo_partida` (más claro)
- `CPAIDES` → `cod_pais` (más claro)
- `VPESNET` → `PesoNeto` (más claro)
- `AÑO` → `año` (minúsculas)

**Ejemplo visual:**

```
ANTES (del Excel):
┌────────────┬──────────┬────┬─────┬──────┐
│ Subpartida │ CPAIDES  │ AÑO│ MES │ FOB  │
├────────────┼──────────┼────┼─────┼──────┤
│ 0201210000 │ 0840     │2026│  02 │15000 │
└────────────┴──────────┴────┴─────┴──────┘

DESPUÉS (renombrado):
┌────────────────┬──────────┬────┬─────┬─────┐
│ codigo_partida │ cod_pais │año │mes  │ fob │
├────────────────┼──────────┼────┼─────┼─────┤
│ 0201210000     │ 0840     │2026│  02 │15000│
└────────────────┴──────────┴────┴─────┴─────┘
```

**Técnica: .rename()**

```python
df.rename(columns={'viejo': 'nuevo'})

# Equivalente manual:
df['codigo_partida'] = df['Subpartida']
del df['Subpartida']

# Pero .rename() es más elegante
```

---

## 🆕 PARTE 2: CREAR CAMPOS DERIVADOS

### Líneas 24-25: Extraer Subcódigos

```python
df['cod_capitulo'] = df['codigo_partida'].str[:2]
df['cuatro_dig'] = df['codigo_partida'].str[:4]
```

**¿Qué hace?**

Extrae primeros N caracteres de `codigo_partida`.

**Ejemplo:**

```
codigo_partida = "0201210000"

.str[:2]  = "02"        ← Capítulo (2 primeros dígitos)
.str[:4]  = "0201"      ← 4 dígitos (4 primeros)

Resultado:
cod_capitulo = "02"
cuatro_dig = "0201"
```

**¿Por qué?**

Porque después necesitarás analizar por:
- Capítulo (categoría general)
- 4 dígitos (más detallado)
- 6 dígitos (aún más detallado)

---

## 📊 PARTE 3: PRIMERA AGREGACIÓN

### Línea 28-29: Variables a Agrupar

```python
variables_a_agrupar_x = ['flujo_comercial','cod_pais','cod_capitulo','codigo_partida','año','mes','CADU','RUC']
df[variables_a_agrupar_x] = df[variables_a_agrupar_x].fillna('NaN_temp')
```

**¿Qué son variables_a_agrupar_x?**

Lista de columnas por las cuales agruparás después.

**fillna('NaN_temp')?**

Problema: Si hay valores FALTANTES (NaN, vacíos):

```python
# Con NaN:
df.groupby(['cod_pais'])
# → Pandas IGNORA filas con NaN en cod_pais
# → Pierdes datos

# Con 'NaN_temp':
df[col].fillna('NaN_temp')  # Reemplaza NaN por texto
# → Pandas INCLUYE la fila en el grupo 'NaN_temp'
# → Recuperas datos
```

**Luego los recuperas:**

```python
base1_x[variables_a_agrupar_x].replace('NaN_temp', np.nan)
# Vuelve a cambiar 'NaN_temp' por NaN
```

**¿Por qué molestarse?**
- Porque algunos RUC pueden estar vacíos
- No los quieres perder
- Los necesitas para contabilidad

---

### Línea 31-34: Groupby (Primera Agregación)

```python
base1_x = df.groupby(variables_a_agrupar_x).agg({
    'fob': 'sum',
    'PesoNeto': 'sum'
}).reset_index()
```

**¿Qué es groupby?**

Agrupa datos por grupos y SUMA valores dentro de cada grupo.

**Ejemplo visual:**

```
ANTES (500 filas):
┌──────────┬────────┬────┬────┬─────┐
│ cod_pais │ año   │ mes│ fob │peso │
├──────────┼────────┼────┼────┼─────┤
│ 0840 (USA)│ 2026 │ 02 │5000 │100  │
│ 0840 (USA)│ 2026 │ 02 │3000 │ 60  │  ← Mismo país, año, mes
│ 0840 (USA)│ 2026 │ 02 │2000 │ 40  │
│ 0876 (MEX)│ 2026 │ 02 │1000 │ 20  │
│ 0876 (MEX)│ 2026 │ 02 │4000 │ 80  │
└──────────┴────────┴────┴────┴─────┘

DESPUÉS (5 filas, agrupadas):
┌──────────┬────────┬────┬──────┬──────┐
│ cod_pais │ año   │ mes│ fob  │ peso │
├──────────┼────────┼────┼──────┼──────┤
│ 0840     │ 2026  │ 02 │ 10000│ 200  │  ← Suma de 3 filas
│ 0876     │ 2026  │ 02 │ 5000 │ 100  │  ← Suma de 2 filas
└──────────┴────────┴────┴──────┴──────┘
```

**Desglose:**

```python
df.groupby([col1, col2, col3])  # Agrupa por estos 3
.agg({                          # Para cada grupo, calcula:
    'fob': 'sum',               # FOB = SUM de todos
    'PesoNeto': 'sum'           # PesoNeto = SUM de todos
})
.reset_index()                  # Convierte índice en columnas
```

**Resultado:**

```python
base1_x:
┌───────────────────┬─────┬──────────────┐
│ Columnas agrupadas│ fob │ PesoNeto     │
├───────────────────┼─────┼──────────────┤
│ (flujo, pais, ...,│sum  │ sum          │
│   año, mes, ...)  │     │              │
└───────────────────┴─────┴──────────────┘
```

**¿Por qué?** 

Porque si tienes 500 transacciones del mismo país/año/mes, las resumes en 1 fila = **VELOCIDAD**.

---

### Línea 36-37: Recuperar NaN

```python
base1_x[variables_a_agrupar_x] = base1_x[variables_a_agrupar_x].replace('NaN_temp', np.nan)
```

Cambia `'NaN_temp'` de vuelta a `np.nan`.

---

### Línea 40-41: Convertir Tipos

```python
base1_x['año'] = base1_x['año'].astype(int)
base1_x['mes'] = base1_x['mes'].astype(int)
```

**¿Por qué?**

Después de groupby, las columnas de agrupamiento quedan como **texto** ("2026" string):

```python
# Sin astype():
base1_x['año'] = ["2026", "2026", "2025"]  # Texto
base1_x['año'] > 2025  # ERROR: no se compara texto con número

# Con astype(int):
base1_x['año'] = [2026, 2026, 2025]  # Números
base1_x['año'] > 2025  # OK: devuelve [True, True, False]
```

---

### Línes 44-45: Filtrar Futuros

```python
logger.debug(f"Eliminando datos posteriores a mes {config.MES_NUM[1]} del año {config.ANIOS[0]}")
base1_x = base1_x[~((base1_x['año']==config.ANIOS[0]) & (base1_x['mes']>=config.MES_NUM[1]))]
```

**¿Qué hace?**

Elimina los datos que están en el FUTURO respecto a hoy.

**Ejemplo:**

```python
Hoy es: 3 de abril
config.ANIOS[0] = 2026
config.MES_NUM[0] = 2  (Febrero)
config.MES_NUM[1] = 3  (Marzo - ELIMINAR)

# NO QUIERO:
(año==2026) & (mes>=3)  # Año 2026 Y mes 3 en adelante
# = Marzo 2026, Abril 2026, Mayo 2026, ...  ← FUTURO

# Quiero MANTENER:
- Enero 2026 ✅
- Febrero 2026 ✅
- Todo de 2025 ✅
- Marzo 2026, Abril 2026, ... ❌
```

**Operador ~:**

```python
# ~ = NOT (negación lógica)
~True = False
~False = True

base1_x[~condicion]  # Mantiene filas donde condicion==False
```

---

### Líneas 48-51: Crear Variable PERIODO (Paso 1)

```python
base1_x['periodo'] = ''
base1_x.loc[base1_x['año'] == config.ANIOS[1]-1, 'periodo'] = str(config.ANIOS[1]-1)
base1_x.loc[base1_x['año'] == config.ANIOS[1], 'periodo'] = str(config.ANIOS[1])

periodo_crear, _ = config.construir_periodos()
base1_x.loc[base1_x['año'] == config.ANIOS[0], 'periodo'] = periodo_crear[1]
```

**¿Qué hace?**

Crea una columna `periodo` que identifica a qué período pertenece cada fila.

**Ejemplo:**

```python
ANIOS = [2026, 2025]
config.MES_NUM = [2, 3]  # Febrero

# Línea 1:
base1_x['periodo'] = ''  # Inicializa vacío

# Línea 2:
# Si año == 2024 (ANIOS[1]-1 = 2025-1):
base1_x.loc[base1_x['año']==2024, 'periodo'] = "2024"

# Línea 3:
# Si año == 2025 (ANIOS[1]):
base1_x.loc[base1_x['año']==2025, 'periodo'] = "2025"

# Línea 5-6:
periodo_crear, _ = config.construir_periodos()
# periodo_crear = ["Ene-feb 25", "Ene-feb 26", "Ult_12_meses"]
# Si año == 2026 (ANIOS[0]):
base1_x.loc[base1_x['año']==2026, 'periodo'] = "Ene-feb 26"  # periodo_crear[1]

RESULTADO:
┌──────┬──────────┐
│ año  │ periodo  │
├──────┼──────────┤
│ 2024 │ "2024"   │
│ 2025 │ "2025"   │
│ 2026 │ "Ene-feb 26" │
└──────┴──────────┘
```

---

### Línea 53: Log

```python
logger.debug(f"Base1 completada: {len(base1_x)} registros con periodos")
```

Registra: "Base1 completada: 150 registros con periodos"

---

## 📊 PARTE 4: SEGUNDA AGREGACIÓN

### Línea 56-57: Filtrar Años Relevantes y Copiar

```python
base2_x = base1_x[(base1_x['año']==config.ANIOS[1]) | (base1_x['año']==config.ANIOS[0])].copy()
```

**¿Qué hace?**

Crea `base2_x` con solo datos de 2025 y 2026 (años "útiles").

**Desglose:**

```python
(base1_x['año']==2025) | (base1_x['año']==2026)
# | = OR (o)
# = Incluye filas donde año == 2025 OR año == 2026
# = Excluye 2024 y anteriores
```

**¿Por qué solo 2025 y 2026?**

Porque necesitas:
- Datos del año ANTERIOR completo (2025) = 12 meses
- Datos del año ACTUAL hasta hoy (2026, solo ene-feb)

---

### Líneas 59-62: Asignar Periodos Acumulados

```python
# Enero-Febrero 2025
base2_x.loc[(base2_x['año']==config.ANIOS[1]) & (base2_x['mes']<=config.MES_NUM[0]), 'periodo'] = periodo_crear[0]

# Últimos 12 meses (ene-feb 2025 + ene-feb 2026)
base2_x.loc[((base2_x['año']==config.ANIOS[1]) & (base2_x['mes']>=config.MES_NUM[1])) | 
            ((base2_x['año']==config.ANIOS[0]) & (base2_x['mes']<=config.MES_NUM[0])), 'periodo'] = periodo_crear[2]
```

**Caso 1: Enero-Febrero 2025**

```python
(año==2025) & (mes<=2)  # 2025 AND mes 1-2
= Enero 2025 + Febrero 2025

periodo = periodo_crear[0]
        = "Ene-feb 25"
```

**Caso 2: Últimos 12 meses**

```
[(año==2025 & mes>=3) OR (año==2026 & mes<=2)]
= [Marzo-Diciembre 2025] + [Enero-Febrero 2026]
= Exactamente 12 meses

periodo = periodo_crear[2]
        = "Ult_12_meses"
```

---

### Línea 65: Marcar año con 0

```python
base2_x.loc[:, 'año'] = 0
```

**¿Por qué?**

Porque después harás CONCAT (concatenación) de base1_x y base2_x.

Si ambos tuvieran año==2026, al concatenar aparecerían DUPLICADOS:

```python
# SIN cambiar año a 0:
base1_x:
year==2025: 100 filas
year==2026: 50 filas  ← Ene-Feb real

base2_x:
year==2025: 50 filas (ene-feb acumulado)
year==2026: 50 filas (últimos 12)

# Cuando concatenas:
year==2026 aparece TRES VECES: base1_x, base2_x (12m), base2_x (ene-feb)

# CON año=0 en base2_x:
base2_x:
year==0: 100 filas (acumulados)

# Cuando concatenas:
year==2026: 50 filas
year==0: 100 filas  ← DISTINGUIBLE
```

---

### Línea 67: Log

```python
logger.debug(f"Base2 completada: {len(base2_x)} registros con periodos acumulados")
```

Registra: "Base2 completada: 200 registros con periodos acumulados"

---

## 📊 PARTE 5: CONCATENAR Y TERCERA AGREGACIÓN

### Línea 70: Concatenar

```python
data_final_x = pd.concat([base1_x, base2_x], axis=0, ignore_index=True)
```

**¿Qué hace?**

Junta dos DataFrames verticalmente.

**Ejemplo:**

```python
base1_x:           base2_x:           data_final_x:
┌─────┐           ┌─────┐           ┌─────┐
│ A   │           │ X   │           │ A   │
│ B   │  +        │ Y   │    =      │ B   │
│ C   │           │ Z   │           │ C   │
└─────┘           └─────┘           │ X   │
                                     │ Y   │
                                     │ Z   │
                                     └─────┘
```

**Parámetros:**

```python
pd.concat([df1, df2], 
          axis=0,              # 0=vertical, 1=horizontal
          ignore_index=True)   # No mantener índices viejos
```

---

### Línea 73-74: Variables para Tercera Agrupación

```python
variables_a_agrupar2_x = ['flujo_comercial','cod_pais','cod_capitulo','codigo_partida','año','CADU','RUC','periodo']
data_final_x[variables_a_agrupar2_x] = data_final_x[variables_a_agrupar2_x].fillna('NaN_temp')
```

Similar a la primera agrupación: lista de columnas para agrupar + reemplazar NaN.

**NOTA: Ahora incluye `periodo`**

---

### Línea 76-79: Tercera Agrupación

```python
data_final_x = data_final_x.groupby(variables_a_agrupar2_x).agg({
    'fob': 'sum',
    'PesoNeto': 'sum'
}).reset_index()
```

Agrupa por todas las variables (incluyendo ahora `periodo`).

**¿Por qué?**

Porque ahora tienes filas DUPLICADAS de base1_x y base2_x:
- base1_x: año=2026, periodo="Ene-feb 26" (detalle)
- base2_x: año=0, periodo="Ult_12_meses" (acumulado)

Necesitas sumarlas por período final.

---

### Línea 81: Recuperar NaN

```python
data_final_x[variables_a_agrupar2_x] = data_final_x[variables_a_agrupar2_x].replace('NaN_temp', np.nan)
```

Vuelve a cambiar `'NaN_temp'` por `np.nan`.

---

### Línea 83: Log Final

```python
logger.info(f"Procesamiento completado. {len(data_final_x)} registros con {data_final_x['periodo'].nunique()} períodos")
```

Registra: "Procesamiento completado. 250 registros con 4 períodos"

---

### Línea 84: Return

```python
return data_final_x
```

Devuelve el DataFrame procesado.

---

## 🎨 DIAGRAMA DE LAS 3 AGREGACIONES

```
ENTRADA (data_loader):
┌────────────────────────────────────────┐
│ DataFrame con 45,000 filas             │
│ Columnas raras: Subpartida, CPAIDES... │
│ NO agrupadas                           │
└────────────────────────────────────────┘

          ↓ RENOMBRAR
┌────────────────────────────────────────┐
│ 45,000 filas                           │
│ Columnas claras: codigo_partida, ...   │
│ + cod_capitulo, cuatro_dig (nuevos)    │
└────────────────────────────────────────┘

    ↓ PRIMERA AGREGACIÓN (groupby)
┌────────────────────────────────────────┐
│ base1_x: ~150 filas                    │
│ Agrupado por: pais, año, mes, partida │
│ Períodos: "2024", "2025", "Ene-feb 26" │
└────────────────────────────────────────┘

    ↓ SEGUNDA AGREGACIÓN (períodos acumulados)
┌────────────────────────────────────────┐
│ base2_x: ~100 filas                    │
│ Agrupado solo 2025-2026                │
│ Períodos: "Ene-feb 25", "Ult_12_meses" │
│ año = 0 (para evitar duplicados)       │
└────────────────────────────────────────┘

    ↓ CONCATENAR
┌────────────────────────────────────────┐
│ data_final_x: ~250 filas               │
│ base1_x + base2_x combinados           │
└────────────────────────────────────────┘

    ↓ TERCERA AGREGACIÓN (agrupa por período)
┌────────────────────────────────────────┐
│ data_final_x: ~200 filas               │
│ Agrupado incluyendo período            │
│ Periodsco finales: 4 períodos distintos│
│ Listo para transformations.py          │
└────────────────────────────────────────┘

SALIDA:
┌────────────────────────────────────────┐
│ DataFrame limpio, agrupado, periódico  │
│ Columnas: flujo, pais, partida,        │
│           período, fob, peso           │
│ Ready for transformations.py           │
└────────────────────────────────────────┘
```

---

## 📋 TABLA RÁPIDA

| Fase | Nombre | Filas | Agrupa por | Períodos |
|------|--------|-------|-----------|----------|
| 1️⃣ | base1_x | ~150 | país, año, mes, partida | 4 (2024, 2025, Ene-feb 26, +1) |
| 2️⃣ | base2_x | ~100 | (2025-2026) + acumulados | Ene-feb 25, Ult_12m |
| 3️⃣ | data_final_x | ~200 | Incluye período | 4 períodos finales |

---

## ⚠️ ERRORES COMUNES

### Error 1: No usar fillna('NaN_temp')

```python
# ❌ SIN fillna('NaN_temp'):
df.groupby(['RUC', 'mes'])
# Fila con RUC=NaN → SE IGNORA (desaparece)

# ✅ CON fillna('NaN_temp'):
df['RUC'].fillna('NaN_temp')  # RUC=NaN → RUC='NaN_temp'
df.groupby(['RUC', 'mes'])
# Fila RUC='NaN_temp' → SE INCLUYE
```

### Error 2: Olvidar astype(int)

```python
# ❌ SIN astype(int):
base1_x['año'] = ["2026", "2025"]  # Texto
base1_x['año'] > 2025  # ERROR

# ✅ CON astype(int):
base1_x['año'] = [2026, 2025]  # Números
base1_x['año'] > 2025  # OK
```

### Error 3: No filtrar mes futuro

```python
# Si hoy es 3 de abril, config.MES_NUM[1] = 4 (Abril)
# SIN filtrar:
base1_x[~((año==2026) & (mes>=4))]

# Mantienes marzo pero INCLUYES abril y siguientes
# MALO: datos futuros

# CON filtrar:
# Elimina todo 2026 con mes >= 4
# = Mantienes solo ene-feb 2026
```

---

## 🎯 RESUMEN

processing.py hace 3 cosas:

```
1️⃣ RENOMBRA: 
   Columnas raras → Nombres claros

2️⃣ AGRUPA 3 VECES:
   base1_x    → Detalle (cada país, mes, partida)
   base2_x    → Acumulados (períodos especiales)
   data_final_x → Consolidado (listo para análisis)

3️⃣ FILTRA:
   Elimina datos del futuro (mes >= MES_NUM[1])
```

**Conexión con config.py:**
- config.ANIOS → Para periodos y filtros
- config.MES_NUM → Para filtro futuro
- config.construir_periodos() → Nombres de periodos

---

## 💡 EJERCICIOS

### Pregunta 1: ¿Cuántas filas es "base1_x"?

```python
# Depende de:
# - Cuántos países únicos
# - Cuántos productos únicos
# - Todos los años disponibles
# - Todos los meses

# Si tienes 500K transacciones de 50 países, ¿cuántas filas base1_x?
```

**Respuesta:** ~100-300 filas (depende datos, pero mucho menos que original)

### Pregunta 2: ¿Por qué asignar año=0 en base2_x?

```python
# Para evitar que cuando hagas groupby después,
# No confundas año=2026 (detalle) con año=2026 (acumulado)
```

**Respuesta:** Porque los distingues: año=2026 vs año=0.

### Pregunta 3: ¿Qué es ~((año==2026) & (mes>=3))?

```python
# ~ = NOT
# (año==2026) & (mes>=3) = Año 2026 Y mes 3+

# ~(AÑO 2026 Y mes 3+) = NOT(Año 2026 Y mes 3+)
#                      = (Año != 2026) OR (mes < 3)
#                      = Mantiene todo excepto futuro
```

**Respuesta:** Mantiene todo EXCEPTO año 2026 con mes >= 3 (futuro).

---

---

# 🔀 transformations.py - Merges y Clasificaciones

## 📍 Ubicación

```
ddpi_rmc/
└─ src/
   └─ transformations.py  ← Este archivo
```

---

## 🎯 ¿Qué es transformations.py?

Es el **maestro clasificador**:

- **Hace 3 merges** con tablas de correlación (país, producto, capítulo)
- **Crea campos derivados** (cinco_dig, millones_fob, miles_TM)
- **Crea 5 variables de clasificación** (producto2, producto21, producto3, grupo2, grupo3, sector2)
- **Define la lógica IF/THEN** que clasifica cada producto

**Analogía:**
```
processing.py     → Limpia y agrupa datos
transformations.py → CLASIFICA y ENRIQUECE datos con información de correlaciones
```

**¿Por qué 5 variables?**

Porque necesitas análisis en 5 "niveles de zoom":
```
NIVEL 1: producto2     → Nombre refinado del producto
NIVEL 2: producto21    → Sub-clasificación pesquera/textil
NIVEL 3: producto3     → Familia textil
NIVEL 4: grupo2        → Agrupación media (Pescado, Confecciones, etc.)
NIVEL 5: grupo3        → Agrupación detallada (Acero, Cerámica, Papel)
EXTRA:   sector2       → Sector amplio (Sidero-Metalúrgico combina 2)
```

---

## 📖 Lectura Línea por Línea

### Línea 1-4: Imports y Logger

```python
import pandas as pd
import logging

logger = logging.getLogger(__name__)
```

Igual que en otros módulos.

---

### Línea 6: Función aplicar_transformaciones()

```python
def aplicar_transformaciones(df, correlac_pais, correlac_prod, correlac_cap):
    """Aplica transformaciones y merges con tablas de correlación."""
```

**Qué recibe:**
- `df` → DataFrame de processing.py (250 registros, ya agrupados)
- `correlac_pais` → DataFrame con info de países
- `correlac_prod` → DataFrame con info de productos
- `correlac_cap` → DataFrame con info de capítulos

**Qué devuelve:**
- `df` modificado con 10 columnas nuevas de clasificación

**¿Cuándo se llama?**
```python
# En pipeline.py:
df = aplicar_transformaciones(df, correlac_pais, correlac_prod, correlac_cap)
```

---

## 🔗 PARTE 1: MERGES (3 uniones con datos externos)

### Línea 10: Merge de País

```python
df = df.merge(correlac_pais, on='cod_pais', how='left')
logger.debug(f"Merge país completado: {len(df)} registros")
```

**¿Qué es merge?**

Unión entre dos DataFrames usando una **columna en común**.

**Ejemplo visual:**

```
df (antes):                    correlac_pais:              df (después):
┌──────────┬────┐            ┌──────────┬─────────────┐   ┌──────────┬───────────────┬─────────────┐
│ cod_pais │fob │            │ cod_pais │ pais_nombre │   │ cod_pais │ fob           │ pais_nombre │
├──────────┼────┤            ├──────────┼─────────────┤   ├──────────┼───────────────┼─────────────┤
│ 0840     │5000│       +    │ 0840     │ USA         │ = │ 0840     │ 5000          │ USA         │
│ 0876     │3000│            │ 0876     │ MÉXICO      │   │ 0876     │ 3000          │ MÉXICO      │
│ 0484     │2000│            │ 0484     │ BRASIL      │   │ 0484     │ 2000          │ BRASIL      │
└──────────┴────┘            └──────────┴─────────────┘   └──────────┴───────────────┴─────────────┘
                              (tabla de búsqueda)          (nuevo: columna pais_nombre)
```

**Parámetros:**

```python
df.merge(
    correlac_pais,           # Tabla con que unif
    on='cod_pais',          # Columna en común
    how='left'              # Si no encuentra, mantiene la fila (con NaN en nuevas columnas)
)
```

**¿Por qué `how='left'`?**

```python
how='left':
- Mantiene TODAS las filas del df original
- Si cod_pais no está en correlac_pais → las nuevas columnas quedan NaN

how='inner':
- Mantiene solo filas que existen en AMBAS
- Si cod_pais no está en correlac_pais → la fila desaparece

# Usamos 'left' porque preferimos mantener datos dudosos (NaN) 
# que perder datos completamente
```

**¿Qué columnas agrega?**

Todas EXCEPTO `cod_pais` (que ya existe). Típicamente:
- `pais` (nombre del país)
- `región` (región del país)
- Otros campos de la tabla de correlación

---

### Líneas 12-13: Merge de Producto

```python
df = df.merge(correlac_prod, on='codigo_partida', how='left')
logger.debug(f"Merge producto completado: {len(df)} registros")
```

**Idéntico al anterior, pero con productos.**

**¿Qué columnas agrega?**

Información sobre cada `codigo_partida`:
- `Producto` (nombre del producto)
- `Grupo` (grupo del producto)
- `Sector` (sector económico: Textil, Pesquero, etc.)
- `Familia_Textil` (si es textil)
- `Clasific_pesquero` (si es pesquero)
- Otras clasificaciones

---

### Líneas 15-16: Merge de Capítulo

```python
df = df.merge(correlac_cap, on='cuatro_dig', how='left')
logger.debug(f"Merge capítulo completado: {len(df)} registros")
```

**Igual, pero por capítulos.**

**Nota:** Usa `cuatro_dig` (primeros 4 dígitos) como columna común.

**¿Por qué capítulo?** 

Porque hay clasificaciones que necesitan el capítulo (2 dígitos) o 4 dígitos.

---

## 🆕 PARTE 2: CAMPOS DERIVADOS

### Línea 18: Crear cinco_dig

```python
df['cinco_dig'] = df['codigo_partida'].str[:5]
```

Extrae los 5 primeros dígitos de `codigo_partida`.

**Ejemplo:**
```
codigo_partida = "0302390000"
.str[:5] = "03023"
```

**¿Por qué?** 

Porque algunas clasificaciones necesitan exactamente 5 dígitos, no 4, no 6.

---

### Línea 21-22: Campos Monetarios

```python
df['millones_fob'] = df['fob'] / 1_000_000
df['miles_TM'] = df['PesoNeto'] / 1_000_000
```

**millones_fob:**
```
fob = 5,000,000 (en dólares)
millones_fob = 5,000,000 / 1,000,000 = 5 (millones de dólares)
```

**miles_TM:**
```
PesoNeto = 2,500,000 (kg)
miles_TM = 2,500,000 / 1,000,000 = 2.5 (miles de TM)
```

**¿Por qué dividir?**

Porque los números en Excel/reportes son más legibles si están en millones/miles.

```
❌ MALO: 5,234,567,000 dólares (confuso)
✅ BUENO: 5,234.57 millones de dólares (claro)
```

---

## 🏷️ PARTE 3: 5 VARIABLES DE CLASIFICACIÓN

### Línea 25: Inicializar producto2

```python
df['producto2'] = df['Producto']
```

Copia el nombre original del producto.

**Luego se sobrescribe** con casos especiales usando `.loc[]`.

---

### Línea 28-55: Lógica IF/THEN (Casos especiales)

Esta es **la parte más importante y densa** de todo el archivo.

**Patrón general:**

```python
df.loc[condición, 'producto2'] = 'nuevo_valor'
```

**Desglose:**

| Parte | Qué hace |
|-------|----------|
| `df.loc[` | Filtra filas donde... |
| `condición` | Se cumple esta cond IÓN |
| `, 'producto2']` | En la columna producto2 |
| `= 'nuevo_valor'` | Ponle este valor |

**Ejemplo 1: Textil**

```python
df.loc[df['Sector']=='Textil', 'producto2'] = df['Familia_Textil']
```

**Significa:**
```
SI Sector == 'Textil' ENTONCES
    producto2 = Familia_Textil
```

**Visual:**

```
df:
┌────────┬──────────────────┐
│ Sector │ Familia_Textil   │
├────────┼──────────────────┤
│ Textil │ "Algodón"        │
│ Textil │ "Poliéster"      │
│ Agro   │ "Frutas"         │
└────────┴──────────────────┘

DESPUÉS:
producto2:
┌──────────────────┐
│ "Algodón"        │  ← Tomó de Familia_Textil
│ "Poliéster"      │  ← Tomó de Familia_Textil
│ "Fruta"          │  ← Mantuvo original
└──────────────────┘
```

**Ejemplo 2: Tungsteno (Metalúrgico)**

```python
df.loc[df['Producto']=='Zinc refinado', 'producto2'] = 'Lingotes de zinc - JUMBO'
```

**Significa:**
```
SI Producto == 'Zinc refinado' ENTONCES
    producto2 = 'Lingotes de zinc - JUMBO'
```

Renombra un producto de su nombre genérico a uno más específico.

---

### Línea 30: Condición Compleja (AND)

```python
df.loc[(df['Producto']=='Barras y perfiles de cobre') & ((df['codigo_partida']=='7407100000') | 
       (df['codigo_partida']=='7407290000')), 'producto2'] = 'Barras de cobre'
```

**Desglose:**

```
(df['Producto']=='Barras y perfiles de cobre')
& = Y (AND)
((df['codigo_partida']=='7407100000') | (df['codigo_partida']=='7407290000'))
                                      | = O (OR)
```

**Traducción:**
```
SI Producto == 'Barras y perfiles de cobre' 
   AND (codigo_partida == '7407100000' OR codigo_partida == '7407290000')
ENTONCES
    producto2 = 'Barras de cobre'
```

**¿Por qué tan específico?**

Porque hay múltiples códigos de partida para "Barras de cobre".

Solo algunos de esos códigos (7407100000, 7407290000) merecen ser llamados "Barras de cobre".

Los otros códigos pueden ser clasificados diferente.

---

### Línea 57: PRODUCTO21

```python
df['producto21'] = df['producto2']

df.loc[df['Sector']=='Pesquero', 'producto21'] = df['Clasific_pesquero']
df.loc[df['Sector']=='Textil', 'producto21'] = df['Material_Textil']
```

**¿Qué es?**

Una **variante** de producto2 que se especializa en:
- **Pesquero:** Muestra clasificación pesquera (¿Qué tipo de pescado?)
- **Textil:** Muestra material textil (¿Algodón? ¿Poliéster?)

**Ejemplo:**

```
Para un producto Textil:

producto2 = "Camiseta de algodón"
producto21 = "Algodón"  ← Material más específico

Para un producto Pesquero:

producto2 = "Anchoveta en conserva"
producto21 = "Anchoveta"  ← Clasificación pesquera
```

**¿Por qué dos?**

Porque a veces necesitas el nombre completo (producto2) y a veces solo el tipo (producto21).

---

### Línea 63: PRODUCTO3

```python
df['producto3'] = df['producto2']
df.loc[df['Sector']=='Textil', 'producto3'] = df['Familia_Textil']
df.loc[(df['Rubro_Textil'].isin(['Textiles', 'Otros'])) & (df['Sector']=='Textil'), 
       'producto3'] = 'Materias textiles'
```

**¿Qué es?**

Especialización para **análisis de familia textil**.

**Línea 2:**
```
Si Sector == 'Textil':
    producto3 = Familia_Textil
```

**Línea 3-4:**
```
Si (Rubro_Textil es 'Textiles' O 'Otros') AND Sector == 'Textil':
    producto3 = 'Materias textiles'  ← Categoría general
```

**Caso de uso:** Cuando necesitas ver textiles vs. otras materias textiles.

---

### Línea 68: GRUPO2 (Agrupación Principal)

```python
df['grupo2'] = df['Grupo']
```

Comienza copiando el `Grupo` original.

**Luego se sobrescribe** con 10+ casos especiales:

#### Caso 1: Siderúrgico y Metalúrgico

```python
df.loc[df['Sector']=='Siderúrgico', 'grupo2'] = 'Siderúrgico'
df.loc[df['Sector']=='Metalúrgico', 'grupo2'] = 'Metalúrgico'
```

Si el sector es esos, mantenlos (o renombra si estaban diferente).

#### Caso 2: Plástico

```python
df.loc[df['cod_capitulo']=='39', 'grupo2'] = 'Plástico'
```

El capítulo 39 de aduanas = **Plástico**.

#### Caso 3: Pesquero - Pescado

```python
df.loc[(((df['cuatro_dig']=='0302') | (df['cuatro_dig']=='0303') | (df['cuatro_dig']=='0304') | 
         (df['cuatro_dig']=='0305') | (df['Producto']=='Conserva de pescado')) & 
        ((df['cinco_dig']!='03029') & (df['cinco_dig']!='03039') & (df['cinco_dig']!='03052') & 
         (df['cinco_dig']!='03057'))) & (df['Sector']=='Pesquero'), 'grupo2'] = 'Pescado'
```

**¡COMPLEJO!** Desglose:

```
(
  (cuatro_dig == '0302' OR '0303' OR '0304' OR '0305') 
  OR Producto == 'Conserva de pescado'
)
AND
(
  cinco_dig != '03029' AND != '03039' AND != '03052' AND != '03057'
)
AND Sector == 'Pesquero'

ENTONCES grupo2 = 'Pescado'
```

**En palabras:**
```
"Si es por aduanas pescado (0302-0305) 
 O es conserva de pescado,
 PERO excluye estos 4 códigos especiales,
 Y está en Pesquero,
 entonces es PESCADO"
```

**¿Por qué excluir 4 códigos?**

Porque esos 4 códigos específicos son **Langostino**, **Pota** y otros, NO pescado común.

#### Caso 4: Textil

```python
df.loc[(df['Rubro_Textil']=='Prendas') & (df['Sector']=='Textil'), 'grupo2'] = 'Confecciones'
df.loc[(df['Rubro_Textil'].isin(['Textiles', 'Otros'])) & (df['Sector']=='Textil'), 'grupo2'] = 'Textiles'
```

Si es textil + Prendas → **Confecciones**
Si es textil + Textiles/Otros → **Textiles**

#### Caso 5: Anchoveta

```python
df.loc[((df['Producto']=='Harina de pescado') | (df['Producto']=='Aceite de pescado')) & 
       (df['Sector']=='Pesquero'), 'grupo2'] = 'Productos de anchoveta'
```

Si es harina O aceite de pescado → **Productos de anchoveta**

---

### Línea 102: GRUPO3 (Agrupación Detallada)

```python
df['grupo3'] = df['Grupo']
```

**Parecida a grupo2, pero con MÁS categorías.**

Ejemplos:

```python
# Acero
df.loc[...condición acero..., 'grupo3'] = 'Productos de acero-total'

# Cerámica
df.loc[..., 'grupo3'] = 'Productos cerámicos'

# Papel
df.loc[..., 'grupo3'] = 'Papel y cartón'

# Vidrio
df.loc[..., 'grupo3'] = 'Vidrios y manufacturas'

# Drogas
df.loc[..., 'grupo3'] = 'Productos de tocador y limpieza'
```

---

### Línea 138: SECTOR2

```python
df['sector2'] = df['Sector']
df.loc[(df['Sector']=='Siderúrgico') | (df['Sector']=='Metalúrgico'), 'sector2'] = 'Sidero-Metalúrgico'
```

**En general:** Mantiene el `Sector` original.

**Excepción especial:** Combina Siderúrgico + Metalúrgico en "**Sidero-Metalúrgico**" para análisis conjunto.

**Resultado:**

```
Sector original         sector2
────────────────       ──────────────────────
Siderúrgico       →    Sidero-Metalúrgico
Metalúrgico       →    Sidero-Metalúrgico
Textil            →    Textil
Pesquero          →    Pesquero
Agropecuario      →    Agropecuario
```

---

## 🎨 DIAGRAMA COMPLETO DEL FLUJO

```
ENTRADA (de processing.py):
┌─────────────────────────────┐
│ df: 250 filas               │
│ Columnas:                   │
│ - codigo_partida, cod_pais  │
│ - fob, PesoNeto             │
│ - período, flujo, etc.      │
│                             │
│ SIN información descriptiva │
└─────────────────────────────┘

          ↓ MERGE 1: País

┌─────────────────────────────┐
│ df: 250 filas               │
│ + pais (nombre), región.... │
└─────────────────────────────┘

          ↓ MERGE 2: Producto

┌─────────────────────────────┐
│ df: 250 filas               │
│ + Producto, Grupo, Sector   │
│ + Familia_Textil,           │
│   Clasific_pesquero         │
└─────────────────────────────┘

          ↓ MERGE 3: Capítulo

┌─────────────────────────────┐
│ df: 250 filas               │
│ + toda info de capítulos    │
│ + industrias, rubros        │
└─────────────────────────────┘

          ↓ CREAR CAMPOS DERIVADOS

┌─────────────────────────────┐
│ df: 250 filas               │
│ + cinco_dig                 │
│ + millones_fob              │
│ + miles_TM                  │
└─────────────────────────────┘

          ↓ APLICAR LÓGICA IF/THEN (95 LINEAS)

┌─────────────────────────────┐
│ df: 250 filas               │
│ + producto2  (refinado)     │
│ + producto21 (pesquero+txt) │
│ + producto3  (familia txt)  │
│ + grupo2     (medio)        │
│ + grupo3     (detallado)    │
│ + sector2    (amplio)       │
│                             │
│ TOTALMENTE CLASIFICADO      │
└─────────────────────────────┘

SALIDA (hacia tables.py):
┌─────────────────────────────┐
│ DataFrame enriquecido con   │
│ 10 columnas nuevas          │
│ Listo para tablas pivote    │
└─────────────────────────────┘
```

---

## 📊 TABLA RESUMEN DE CLASIFICACIONES

| Variable | Propósito | Niveles | Ejemplo |
|----------|-----------|---------|---------|
| `Producto` (original) | Nombre genérico | Muchos | "Zinc refinado" |
| `producto2` | Refinado | ~40 | "Lingotes de zinc - JUMBO" |
| `producto21` | Pesquero/Textil esp. | Específico | "Algodón", "Anchoveta" |
| `producto3` | Familia textil | Textil only | "Materias textiles" |
| `grupo2` | Agrupación media | 15 categorías | "Confecciones", "Pescado" |
| `grupo3` | Agrupación detallada | 20 categorías | "Acero", "Papel", "Cerámica" |
| `sector2` | Sector amplio | 6-7 | "Sidero-Metalúrgico" |

---

## ⚠️ ERRORES COMUNES

### Error 1: Confundir producto2 con producto21

```python
# ❌ MALO (usando product2 cuando necesitas específico):
df.groupby('producto2')  # Te da "Barras de cobre" genérico

# ✅ BUENO (si necesitas material):
df.groupby('producto21')  # Te da "Algodón", "Cobre puro", etc.
```

### Error 2: Olvidar que .loc modifica IN-PLACE

```python
# ❌ MALO:
df['producto2'] = ...
df.loc[condición, 'producto2'] = ...  # ← Sobrescribe lo anterior

# ✅ BUENO:
# Primero copies, luego modificas condicionalmente
# Por eso empieza con: df['producto2'] = df['Producto']
```

### Error 3: Excluir exclusiones (cinco_dig != '03029')

```python
# Esta línea:
(df['cinco_dig']!='03029') & (df['cinco_dig']!='03039') & ...

# Significa EXCLUIR estos 4 códigos
# Si no entiendes esto, acabas incluyendo lo que querías excluir
```

### Error 4: Confundir | (OR) con & (AND)

```python
# ❌ MALO:
df.loc[(df['Sector']=='Textil') & (df['Sector']=='Pesquero'), 'grupo2'] = ...
# Condición IMPOSIBLE: no puede ser Textil AND Pesquero simultáneamente

# ✅ BUENO:
df.loc[(df['Sector']=='Textil') | (df['Sector']=='Pesquero'), 'grupo2'] = ...
# Textil OR Pesquero (puede ser uno u otro)
```

---

## 🎯 RESUMEN

transformations.py hace 3 cosas principales:

```
1️⃣ MERGES:
   - Trae información de países
   - Trae información de productos
   - Trae información de capítulos

2️⃣ CAMPOS DERIVADOS:
   - cinco_dig (para códigos específicos)
   - millones_fob (para reportes)
   - miles_TM (para reportes)

3️⃣ CLASIFICACIÓN (5 variables):
   - producto2  (refinado)
   - producto21 (pesquero/textil específico)
   - producto3  (familia textil)
   - grupo2     (agrupación media)
   - grupo3     (agrupación detallada)
   - sector2    (sector amplio: Sidero-Metalúrgico)
```

**Conexión con otros módulos:**
- **processing.py** → Entrega datos agrupados
- **transformations.py** → Los ENRIQUECE con correlaciones y clasificaciones
- **tables.py** → Los TABULA por periodo, país, grupo, etc.

---

## 💡 EJERCICIOS

### Pregunta 1: ¿Qué diferencia hay entre merge con how='left' vs how='inner'?

```python
# df tiene 250 filas, pero solo 240 coinciden en correlac_pais

# how='left':  → 250 filas (10 con NaN)
# how='inner': → 240 filas (sin los 10)

# ¿Cuál es mejor?
```

**Respuesta:** Depende del caso, pero 'left' es más seguro: mantiene datos aunque sean incompletos.

### Pregunta 2: ¿Por qué crear producto2 si ya existe Producto?

```python
# Porque Producto es genérico del aduanal
# Pero el análisis necesita nombres específicos del negocio

# Producto = "Zinc refinado" (aduanal)
# producto2 = "Lingotes de zinc - JUMBO" (comercial)
```

**Respuesta:** Producto es genérico (aduanal), producto2 es el que USA tu empresa para análisis.

### Pregunta 3: ¿Qué significa esta línea?

```python
df.loc[(df['cinco_dig']!='03029') & (df['cinco_dig']!='03039') & 
       (df['cinco_dig']!='03052') & (df['cinco_dig']!='03057'), 'grupo2'] = 'Pescado'
```

**Respuesta:** "Agrupa como Pescado si el código de 5 dígitos NO es ninguno de estos 4 especiales".

---

**Te queda claro el flujo completo de:**
- config.py → data_loader.py → processing.py → transformations.py → tables.py → excel_writer.py

**¿Quieres profundizar en tables.py o excel_writer.py?** 👇

---

# 📊 EXPLICACIÓN DE `tables.py`

Si `transformations.py` fue el módulo que "ordenó y clasificó" la data, entonces `tables.py` es el módulo que la **convierte en tablas listas para reportar**.

En otras palabras:

```python
transformations.py  → deja columnas limpias y clasificadas
tables.py           → resume esas columnas en tablas pivot
excel_writer.py     → escribe esas tablas dentro del Excel
```

---

## 1️⃣ ¿Qué hace realmente `tables.py`?

Hace 5 tipos de resumen:

```python
1. tabla_sectorial()   → resumen total del sector
2. tabla_grupos()      → resumen por grupos dentro del sector
3. tabla_productos()   → resumen por productos dentro del grupo
4. ranking_destinos()  → top países o bloques destino
5. numero_destinos()   → cuántos destinos únicos hubo
```

Es decir: toma una base "larga" y la convierte en reportes "anchos".

Ejemplo:

```python
# Entrada (larga)
sector2   periodo         millones_fob
Textil    2025            10
Textil    Ene 25          12
Textil    Ene 26          15
Textil    Ult_12_meses    60

# Salida (ancha)
           2025   Ene 25   Ene 26   Ult_12_meses
Textil      10      12       15         60
```

Eso es exactamente lo que hace `pivot_table()`.

---

## 2️⃣ `tabla_sectorial()`

### ¿Para qué sirve?

Genera la fila principal del sector completo.

Ejemplo conceptual para Textil:

```python
Textil | FOB 2025 | FOB Ene25 | FOB Ene26 | FOB Ult12m | TM Ene25 | TM Ene26
```

### Paso a paso

#### Paso 1: filtra solo el sector pedido

```python
datos_filtrados = df[(df['sector2']==sector) & (df['periodo'].isin(periodos))]
```

Si `sector = 'Textil'`, solo sobreviven las filas textiles.

#### Paso 2: crea una tabla pivote

```python
tabla = datos_filtrados.pivot_table(
    index=['flujo_comercial', 'flujo_comercial2', 'flujo_comercial3', 'sector2'],
    columns='periodo',
    values=['millones_fob','miles_TM'],
    aggfunc='sum'
)
```

Esto significa:

```python
index   = qué va a identificar la fila
columns = qué va a convertirse en columnas
values  = qué números quieres sumar
aggfunc = cómo agregas (sumar)
```

### ¿Por qué usa varios `flujo_comercial`?

Porque la plantilla histórica del Excel está diseñada para varios niveles de filas, y este índice múltiple permite conservar esa estructura aunque en la práctica el valor sea casi siempre `"EXPORTACION"`.

### ¿Qué sale de aquí?

Algo así:

```python
                         millones_fob                     miles_TM
periodo                       2025  Ene 25  Ene 26 ...   Ene 25  Ene 26
EXPORTACION EXPORTACION ...
Textil                         100    120     140          20      25
```

### Luego selecciona columnas específicas

```python
columnas_miles_TM = [col for col in tabla.columns if col[1] in periodos_miles_TM and col[0]=='miles_TM']
columnas_millones_fob = [col for col in tabla.columns if col[0]=='millones_fob']
tabla_final = tabla[columnas_millones_fob + columnas_miles_TM]
```

Aquí hay una decisión de negocio importante:

```python
FOB      → usa todos los períodos
TM       → usa solo algunos períodos (periodos_miles_TM)
```

No es casualidad. Se hace así porque la plantilla no siempre muestra TM en todas las columnas.

---

## 3️⃣ `tabla_grupos()`

### ¿Para qué sirve?

Genera las filas de los grupos principales dentro del sector.

Ejemplo:

```python
Textil
├─ Confecciones
└─ Textiles
```

### Lógica

Recibe una lista de grupos ya ordenados por importancia desde `pipeline.py`:

```python
grupos = [g for g in flujo_grupo_ordenado.index if g != "NA"][:2]
```

Eso significa:

```python
1. agrupa por grupo2
2. suma FOB
3. ordena de mayor a menor
4. toma los 2 más importantes
```

Luego `tabla_grupos()` repite la lógica de pivote para cada grupo y concatena los resultados:

```python
tablas_grupos = pd.concat([tablas_grupos, tabla_grupo_final])
```

### Idea importante

`tabla_sectorial()` devuelve la fila "padre" del sector.

`tabla_grupos()` devuelve las filas "hijas" de los grupos.

Después, en el pipeline, ambas se apilan:

```python
tabla_5 = pd.concat([tabla_1, tabla_3])
```

Entonces obtienes una tabla final como:

```python
Fila 1: Textil
Fila 2: Confecciones
Fila 3: Textiles
```

Y esa estructura es la que `excel_writer.py` copia en el Excel.

---

## 4️⃣ `tabla_productos()`

Este método está preparado para un nivel aún más detallado.

### ¿Qué hace?

Construye:

```python
1. una fila resumen del producto2
2. hasta 3 subproductos detallados usando producto21
```

Ejemplo:

```python
producto2   = "Prendas de vestir"
producto21  = "Algodón", "Sintético", "Mezcla"
```

Entonces podría producir:

```python
Prendas de vestir        ← resumen total
Algodón                  ← detalle 1
Sintético                ← detalle 2
Mezcla                   ← detalle 3
```

### ¿Por qué hace dos pivotes?

Porque uno responde a un nivel distinto del otro:

```python
tabla_prod          → resumen por producto2
tabla_prod_producto → detalle por producto21
```

### ¿Por qué usa `.head(3)`?

```python
tabla_prod_producto = tabla_prod_producto.sort_values(
    by=('millones_fob', periodo_orden),
    ascending=False
).head(3)
```

Porque el reporte no quiere todos los subdetalles posibles, sino solo los 3 más importantes.

Es una decisión de negocio, no una limitación técnica.

---

## 5️⃣ `ranking_destinos()`

### ¿Qué hace?

Crea una tabla con:

```python
1. una fila del sector total
2. las 5 filas de principales destinos
```

### ¿Qué usa como destino?

```python
index='Pais_UE27'
```

Ojo: no usa `Pais` sino `Pais_UE27`.

Eso significa que el ranking puede ser por:

```python
UE27
ASIA
EEUU
OTROS
```

o por el nombre que venga en esa columna según tu correlacionador.

### ¿Cómo lo arma?

Primero:

```python
tabla_sector = data_filtrada.pivot_table(index='sector2', ...)
```

Eso da el total del sector.

Luego:

```python
tabla_paises = data_filtrada.pivot_table(index='Pais_UE27', ...)
```

Eso da los destinos.

Después:

```python
tabla_paises = tabla_paises.sort_values(...).head(5)
```

Y finalmente:

```python
tabla_final = pd.concat([tabla_sectores, tabla_paises_final])
```

Queda así:

```python
Fila 1: Textil
Fila 2: EEUU
Fila 3: ASIA
Fila 4: UE27
...
```

Por eso en `excel_writer.py` muchas veces se empieza a leer desde `index[x+1]`: la fila 0 es el total del sector, y las siguientes son los destinos.

---

## 6️⃣ `numero_destinos()`

Este método responde una pregunta muy concreta:

```python
¿Cuántos países distintos compraron exportaciones de este sector?
```

### Código clave

```python
resultado = df[(df['periodo'].isin(periodos)) &
               (df['sector2'].isin(sectores)) &
               (df['millones_fob'] > 0)] \
               .groupby(['sector2', 'periodo']) \
               .agg(Numero_Destinos=('Pais', 'nunique')) \
               .unstack()
```

### Traducción humana

```python
1. filtra solo los períodos deseados
2. filtra solo los sectores deseados
3. elimina filas con FOB = 0
4. agrupa por sector y período
5. cuenta países únicos
6. convierte el resultado en formato ancho
```

### ¿Qué significa `nunique`?

```python
nunique = number of unique values
```

Ejemplo:

```python
Pais
Perú
Chile
Chile
EEUU

nunique = 3
```

No cuenta filas, cuenta países distintos.

---

## 7️⃣ Error típico en `tables.py`

### Error 1: creer que `pivot_table()` solo reordena

No. También agrega.

```python
aggfunc='sum'
```

Si tienes 20 filas para el mismo sector/período, las suma.

### Error 2: olvidar que `head(5)` corta información

En ranking:

```python
.head(5)
```

Eso significa que el país 6 ya no aparece aunque sí exista en la base.

### Error 3: pensar que el orden de filas es aleatorio

No lo es:

```python
sort_values(by=('millones_fob', periodo_orden), ascending=False)
```

El ranking depende del período usado para ordenar.

Si cambias `periodo_orden`, cambia el top.

---

# 🧾 EXPLICACIÓN DE `excel_writer.py`

Si `tables.py` arma las tablas, `excel_writer.py` es quien las **copia celda por celda dentro de la plantilla Excel**.

No calcula nada nuevo.

Solo hace esto:

```python
1. abre la plantilla
2. ubica la hoja correcta
3. toma valores del DataFrame
4. los coloca en coordenadas exactas (fila, columna)
5. guarda el archivo final
```

---

## 8️⃣ `generar_reporte()`

Esta es la función principal del módulo.

### ¿Qué hace?

```python
template = config.TEMPLATES / f"Cuadros de RMC-{config.MES_ACTUAL}-{config.ANIOS[0]}-Joel-act.xlsx"
output = config.OUTPUT_REPORTES / f"RMC_{config.MES_ACTUAL}_{config.ANIOS[0]}.xlsx"
```

Construye:

```python
1. la ruta de la plantilla base
2. la ruta donde se guardará el reporte nuevo
```

Luego:

```python
libro = load_workbook(template)
```

Carga el archivo Excel en memoria.

Después extrae las tablas:

```python
tabla_final = tablas['tabla_final']
tabla_destinos = tablas['tabla_destinos']
num_destinos = tablas['num_destinos']
```

Y llama a la función especializada:

```python
_escribir_comercio_textil(...)
```

Finalmente:

```python
libro.save(output)
```

Guarda el Excel completo ya rellenado.

---

## 9️⃣ ¿Por qué hay funciones separadas por hoja?

Porque cada hoja de la plantilla tiene posiciones distintas.

Ejemplo:

```python
Comercio_Agro    → escribe grupos en filas 11 y 26
Comercio_Textil  → escribe grupos en filas 12 y 17
comercio_Pesca   → destinos desde fila 37
```

Entonces no basta con tener un solo "writer" genérico.

Cada hoja necesita su propio mapa de coordenadas.

---

## 🔟 `_escribir_comercio_textil()`

Esta función es especialmente importante en tu proyecto actual.

### Parte 1: filas principales

```python
row_map = {0: 10, 1: 12, 2: 17}
```

Esto significa:

```python
fila del DataFrame 0 → fila 10 del Excel
fila del DataFrame 1 → fila 12 del Excel
fila del DataFrame 2 → fila 17 del Excel
```

No es un patrón matemático continuo.

Es un "mapa manual" basado en cómo está diseñada la plantilla.

### ¿Qué contiene cada una?

Usualmente:

```python
0 → total sector Textil
1 → primer grupo principal
2 → segundo grupo principal
```

### Parte 2: escribir FOB y TM

```python
for t in range(0, 3):
    hoja.cell(row, 8+t).value = tabla_final.iloc[idx, t]
for t in range(0, 2):
    hoja.cell(row, 13+t).value = tabla_final.iloc[idx, t+4]
```

Eso se traduce en:

```python
Columnas H, I, J   → primeros 3 valores
Columnas M, N      → últimos 2 valores de TM
```

Recuerda:

```python
8  = columna H
9  = columna I
10 = columna J
13 = columna M
14 = columna N
```

### Parte 3: destinos

```python
for x in range(0, 3):
    hoja.cell(24+x, 6).value = _index_label(tabla_destinos.index[x+1])
```

Esto significa:

```python
Fila 24 Excel ← destino #1
Fila 25 Excel ← destino #2
Fila 26 Excel ← destino #3
```

Y usa `x+1` porque:

```python
tabla_destinos.iloc[0] = total del sector
tabla_destinos.iloc[1] = primer destino real
```

### Parte 4: número de destinos

```python
for t in range(0, 3):
    hoja.cell(27, 8+t).value = num_destinos.iloc[0, t]
```

Escribe 3 valores horizontales en la fila 27.

---

## 1️⃣1️⃣ `_index_label()`

Esta función parece pequeña, pero resuelve un problema real:

los índices de un `pivot_table()` muchas veces no son strings simples sino tuplas.

Ejemplo:

```python
('EXPORTACION', 'EXPORTACION', 'Textil', 'Confecciones')
```

Si escribieras eso directo en Excel, saldría feo e inútil.

Entonces `_index_label()` hace esto:

```python
1. si el índice es tupla
2. la recorre desde el final
3. devuelve el último valor no vacío
```

Resultado:

```python
'Confecciones'
```

Eso hace que el Excel muestre etiquetas limpias.

---

## 1️⃣2️⃣ `_escribir_comercio_agro()` y `_escribir_comercio_pesca()`

Siguen exactamente la misma filosofía que Textil:

```python
1. toman filas concretas del DataFrame
2. las colocan en coordenadas exactas del Excel
3. insertan destinos
4. insertan número de destinos
```

La diferencia no es conceptual.

La diferencia es puramente de plantilla:

```python
Agro   → otra hoja, otras filas
Pesca  → otra hoja, otras filas
Textil → otra hoja, otras filas
```

---

## 1️⃣3️⃣ Error típico en `excel_writer.py`

### Error 1: pensar que `.iloc[0]` siempre es el primer destino

No.

En varias tablas:

```python
iloc[0] = total sector
iloc[1] = primer destino o primer grupo
```

Si te equivocas aquí, escribes el total donde debería ir un país.

### Error 2: mover columnas sin revisar la plantilla

```python
hoja.cell(10, 8)
```

Eso no es un número arbitrario.

Es la celda exacta esperada por la plantilla.

Si cambias `8` por `7`, desalineas todo el reporte.

### Error 3: abrir el Excel mientras el script quiere guardar

En Windows, si el archivo está abierto, `openpyxl` puede fallar con:

```python
Permission denied
```

No es que el cálculo esté mal.

Es que Excel está bloqueando la sobrescritura del archivo.

---

## 🔗 Conexión final entre `tables.py` y `excel_writer.py`

La relación es esta:

```python
tables.py
    ↓
genera DataFrames con forma exacta
    ↓
excel_writer.py
    ↓
los copia en celdas exactas del Excel
```

Si `tables.py` sale mal:

```python
- faltan filas
- sobran filas
- el orden cambia
- las columnas no coinciden
```

Entonces `excel_writer.py` escribirá datos equivocados aunque su lógica esté "bien".

Y si `tables.py` está bien pero `excel_writer.py` apunta a celdas incorrectas:

```python
- el dato existe
- pero aparece en el lugar equivocado
```

Por eso estos dos módulos siempre deben entenderse juntos.

---

## 🎯 RESUMEN FINAL

```python
config.py
    define rutas y períodos

data_loader.py
    carga archivos

processing.py
    limpia y agrega base

transformations.py
    clasifica y enriquece columnas

tables.py
    resume la base en tablas pivot

excel_writer.py
    coloca esas tablas en la plantilla Excel
```

La idea central es:

```python
Datos crudos
→ datos procesados
→ datos clasificados
→ tablas
→ Excel final
```

---

**Si quieres, el siguiente paso puede ser uno de estos dos:**

- seguir completando `CONFIG_EXPLICADA.md` con una sección igual de detallada sobre `indices_generator.py`
- o rehacer todo el documento para que quede más ordenado, sin caracteres raros de codificación y con una estructura más limpia

---

# 👕 LÓGICA DE `aplicar_transformaciones()` CENTRADA EN TEXTIL

Ahora sí vamos a enfocarnos solo en lo que pasa cuando una fila pertenece al sector `Textil`.

La idea clave es esta:

```python
La base original trae códigos y nombres bastante "aduanales"
↓
aplicar_transformaciones() los convierte en categorías de negocio
↓
esas categorías luego alimentan las tablas y el Excel
```

En Textil esto es especialmente importante, porque no basta con saber:

```python
Producto = "T-shirts de punto, de algodón"
```

El reporte final quiere verlo más bien como:

```python
grupo2     = "Confecciones"
producto2  = "Prendas de vestir"
producto21 = "Algodón"
producto3  = "Prendas de vestir"
```

Es decir:

```python
de un producto aduanal específico
→ pasas a una familia comercial
→ luego a un material
→ luego a un bloque del reporte
```

---

## 1️⃣ ¿Qué problema resuelve esta función para Textil?

La base cruda no viene lista para el cuadro.

Una fila textil puede venir así:

```python
codigo_partida = 6109100031
Producto = "T-shirts de punto, de algodón"
Sector = "Textil"
Grupo = "Confecciones"
```

Pero el reporte no quiere listar todas las partidas una por una.

Quiere algo mucho más resumido, como:

```python
Confecciones
└─ Prendas de vestir
   └─ Algodón
```

Entonces `aplicar_transformaciones()` hace justamente eso:

```python
1. une la base con correlacionadores
2. trae columnas textiles auxiliares
3. redefine nombres para análisis
4. crea agrupaciones que luego usarán tables.py y excel_writer.py
```

---

## 2️⃣ Los merges: ¿por qué son tan importantes para Textil?

Antes de clasificar nada, la función hace merges con 3 correlacionadores:

```python
df = df.merge(correlac_pais, on='cod_pais', how='left')
df = df.merge(correlac_prod, on='codigo_partida', how='left')
df = df.merge(correlac_cap, on='cuatro_dig', how='left')
```

Para Textil, el merge más importante es este:

```python
df = df.merge(correlac_prod, on='codigo_partida', how='left')
```

Porque ahí llegan columnas como:

```python
Producto
Sector
Grupo
Familia_Textil
Material_Textil
Rubro_Textil
```

Sin esas columnas, la lógica textil no existe.

Es decir:

```python
codigo_partida = 6109100031
```

por sí solo no te dice mucho.

Pero tras el merge puede transformarse en algo así:

```python
Producto         = "T-shirts de punto, de algodón"
Sector           = "Textil"
Familia_Textil   = "Prendas de vestir"
Material_Textil  = "Algodón"
Rubro_Textil     = "Prendas"
```

Y recién con eso ya puedes construir un cuadro entendible.

---

## 3️⃣ Normalización técnica antes del merge

Estas líneas parecen técnicas, pero son fundamentales:

```python
df['codigo_partida'] = df['codigo_partida'].astype(str).str.zfill(10)
df['cuatro_dig'] = df['cuatro_dig'].astype(str).str.zfill(4)
```

### ¿Por qué importan tanto en Textil?

Porque los códigos de partida son la llave de clasificación.

Si una partida viene así:

```python
610910031
```

en vez de:

```python
0610910031
```

o si le faltan ceros a la izquierda, el merge no va a encontrar coincidencia.

Y si no encuentra coincidencia:

```python
Familia_Textil  = NaN
Material_Textil = NaN
Rubro_Textil    = NaN
```

Y entonces todo lo demás se cae.

---

## 4️⃣ `cinco_dig`: por qué se crea aunque en Textil casi no se use

```python
df['cinco_dig'] = df['codigo_partida'].str[:5]
```

Esta columna se usa más en pesca, pero forma parte del set de variables derivadas generales.

En Textil no es la columna protagonista.

La protagonista real para textil es más bien:

```python
Familia_Textil
Material_Textil
Rubro_Textil
```

---

## 5️⃣ Variables monetarias: por qué se escalan

```python
df['millones_fob'] = df['fob'] / 1_000_000
df['miles_TM'] = df['PesoNeto'] / 1_000_000
```

Esto no cambia la clasificación textil, pero sí el formato del reporte.

Textil en Excel se muestra como:

```python
US$ Millones
Miles de TM
```

Entonces estas variables son las que usarán después:

```python
tabla_sectorial()
tabla_grupos()
detalle_textil()
ranking_destinos()
indices_generator.py
```

---

## 6️⃣ `producto2`: la gran clasificación comercial de Textil

Aquí empieza la lógica más importante para tu sector:

```python
df['producto2'] = df['Producto']
df.loc[df['Sector']=='Textil', 'producto2'] = df['Familia_Textil']
```

### ¿Qué significa eso?

Primero, `producto2` nace como copia de `Producto`.

Pero si la fila es `Textil`, entonces deja de usar el nombre aduanal específico y pasa a usar `Familia_Textil`.

Ejemplo:

```python
Producto         = "T-shirts de punto, de algodón"
Familia_Textil   = "Prendas de vestir"
```

Entonces:

```python
producto2 = "Prendas de vestir"
```

### Traducción de negocio

Esto convierte miles de partidas textiles específicas en unas pocas familias grandes.

En vez de reportar:

```python
- T-shirts
- camisas
- blusas
- prendas diversas
```

el reporte las resume en:

```python
Prendas de vestir
```

Ese es el nombre que luego aparece en filas como:

```python
Prendas de vestir
Fibras textiles
Tejidos
Hilos e hilados
```

---

## 7️⃣ Ajustes finos dentro de `producto2` para Textil

Luego agregaste estas dos líneas:

```python
df.loc[(df['Sector']=='Textil') & (df['producto2']=='fibras'), 'producto2'] = 'Fibras textiles'
df.loc[(df['Sector']=='Textil') & (df['producto2']=='Otras prendas'), 'producto2'] = 'Otras confecciones'
```

### ¿Por qué fueron necesarias?

Porque `Familia_Textil` venía con nombres que no calzaban perfecto con la plantilla.

Por ejemplo:

```python
Familia_Textil = "fibras"
```

pero tu reporte espera ver:

```python
Fibras textiles
```

Y también:

```python
Familia_Textil = "Otras prendas"
```

pero la plantilla tiene:

```python
Otras confecciones
```

Entonces estas líneas no cambian el fondo del dato.

Lo que hacen es:

```python
alinear el nombre de negocio con el nombre del cuadro Excel
```

---

## 8️⃣ `producto21`: el segundo nivel de detalle textil

```python
df['producto21'] = df['producto2']
df.loc[df['Sector']=='Textil', 'producto21'] = df['Material_Textil']
```

### ¿Qué representa para Textil?

`producto2` te da la familia.

`producto21` te da el material.

Ejemplo:

```python
producto2  = "Prendas de vestir"
producto21 = "Algodón"
```

o:

```python
producto2  = "Tejidos"
producto21 = "Algodón"
```

### ¿Por qué esto es tan útil?

Porque permite construir niveles como estos:

```python
Prendas de vestir
└─ Prendas de algodón

Tejidos
└─ De algodón
```

Es exactamente la lógica que luego usamos en el detalle textil.

Sin `producto21`, sabrías la familia, pero no sabrías el material.

---

## 9️⃣ `producto3`: una mirada alternativa pensada para Textil

```python
df['producto3'] = df['producto2']
df.loc[df['Sector']=='Textil', 'producto3'] = df['Familia_Textil']
df.loc[(df['Rubro_Textil'].isin(['Textiles', 'Otros'])) & (df['Sector']=='Textil'),
       'producto3'] = 'Materias textiles'
```

### ¿Qué está haciendo aquí?

Para Textil, `producto3` crea una clasificación alternativa.

No está pensada para reemplazar a `producto2`, sino para dar otra forma de agrupar.

### Caso clave

Si el `Rubro_Textil` es:

```python
Textiles
Otros
```

entonces:

```python
producto3 = "Materias textiles"
```

### ¿Por qué?

Porque desde el punto de vista analítico a veces conviene separar:

```python
Confecciones terminadas
vs
Materias textiles / insumos textiles
```

Entonces `producto3` te da una mirada más conceptual:

```python
producto2 = detalle comercial
producto3 = mirada más agrupada del negocio textil
```

---

## 🔟 `grupo2`: el gran bloque del reporte textil

Aquí está la división que más manda sobre tu cuadro:

```python
df['grupo2'] = df['Grupo']
...
df.loc[(df['Rubro_Textil']=='Prendas') & (df['Sector']=='Textil'), 'grupo2'] = 'Confecciones'
df.loc[(df['Rubro_Textil'].isin(['Textiles', 'Otros'])) & (df['Sector']=='Textil'), 'grupo2'] = 'Textiles'
```

### ¿Qué significa esto?

Toda fila textil termina cayendo en uno de estos dos grandes bloques:

```python
Confecciones
Textiles
```

### Ejemplo práctico

Si una fila tiene:

```python
Rubro_Textil = "Prendas"
```

entonces:

```python
grupo2 = "Confecciones"
```

Si una fila tiene:

```python
Rubro_Textil = "Textiles"
```

o:

```python
Rubro_Textil = "Otros"
```

entonces:

```python
grupo2 = "Textiles"
```

### ¿Por qué esto es tan importante?

Porque en tu hoja `Comercio_Textil`, las dos filas grandes son justamente:

```python
Confecciones
Textiles
```

O sea:

```python
grupo2 no es una columna más
grupo2 es la columna que define la estructura central del cuadro textil
```

---

## 1️⃣1️⃣ `grupo3`: agrupación todavía más amplia para Textil

```python
df.loc[df['Sector']=='Textil', 'grupo3'] = 'Textil-confecciones'
```

### ¿Qué hace?

Le pone a todas las filas textiles el mismo gran rótulo:

```python
grupo3 = "Textil-confecciones"
```

### ¿Para qué serviría?

Para análisis más macro, cuando no quieres separar:

```python
Confecciones
Textiles
familias
materiales
```

y solo quieres un paraguas general.

Entonces:

```python
grupo2 = nivel operativo del reporte
grupo3 = nivel macro del sector
```

---

## 1️⃣2️⃣ `sector2`: por qué en Textil casi no cambia

```python
df['sector2'] = df['Sector']
df.loc[(df['Sector']=='Siderúrgico') | (df['Sector']=='Metalúrgico'), 'sector2'] = 'Sidero-Metalúrgico'
```

En Textil no hay una reasignación especial.

Entonces:

```python
Sector  = "Textil"
sector2 = "Textil"
```

### ¿Por qué importa igual?

Porque todas las tablas luego filtran con `sector2`, por ejemplo:

```python
df[df['sector2']=='Textil']
```

Así que aunque en Textil no cambie el nombre, sí es la llave formal que usan los módulos siguientes.

---

## 1️⃣3️⃣ Ejemplo completo de una fila textil

Imagina que entra una fila así:

```python
codigo_partida   = 6109100031
Producto         = "T-shirts de punto, de algodón"
Sector           = "Textil"
Grupo            = "Confecciones"
Familia_Textil   = "Prendas de vestir"
Material_Textil  = "Algodón"
Rubro_Textil     = "Prendas"
fob              = 1200000
PesoNeto         = 4500
```

Después de `aplicar_transformaciones()` quedaría aproximadamente así:

```python
producto2     = "Prendas de vestir"
producto21    = "Algodón"
producto3     = "Prendas de vestir"
grupo2        = "Confecciones"
grupo3        = "Textil-confecciones"
sector2       = "Textil"
millones_fob  = 1.2
miles_TM      = 0.0045
```

Y luego eso alimenta:

```python
tabla_sectorial()   → total Textil
tabla_grupos()      → Confecciones
detalle_textil()    → Prendas de vestir / Prendas de algodón
ranking_destinos()  → EEUU, UE, etc.
indices_generator() → subpartidas textiles
```

---

## 1️⃣4️⃣ La lógica jerárquica real del sector textil

Si lo resumimos, tu transformación textil trabaja así:

```python
Nivel 1: sector2
→ Textil

Nivel 2: grupo2
→ Confecciones / Textiles

Nivel 3: producto2
→ Prendas de vestir / Fibras textiles / Tejidos / Hilos e hilados / Otras confecciones

Nivel 4: producto21
→ Algodón / Lana y pelo fino / Sintéticas / Otros
```

Esa jerarquía es la razón por la que luego puedes construir cuadros como:

```python
Textil
├─ Confecciones
│  ├─ Prendas de vestir
│  │  └─ Prendas de algodón
│  └─ Otras confecciones
│     └─ Mantas de pelo fino
└─ Textiles
   ├─ Fibras textiles
   ├─ Tejidos
   │  └─ De algodón
   └─ Hilos e hilados
```

---

## 1️⃣5️⃣ Qué pasaría si faltan columnas textiles en el correlacionador

Si `correlac_prod` no trae bien estas columnas:

```python
Familia_Textil
Material_Textil
Rubro_Textil
```

entonces la transformación textil pierde casi toda su inteligencia.

Podría pasar algo así:

```python
producto2  = NaN
producto21 = NaN
grupo2     = Grupo original o mal asignado
```

Y luego en el reporte verías:

```python
- filas vacías
- grupos incorrectos
- detalles que no aparecen
```

Por eso para Textil el correlacionador de productos es prácticamente el corazón de la clasificación.

---

## 🎯 Resumen final solo para Textil

`aplicar_transformaciones()` en Textil hace esto:

```python
1. usa codigo_partida para traer Familia_Textil, Material_Textil y Rubro_Textil
2. convierte el producto aduanal en una familia comercial (producto2)
3. convierte esa familia en un detalle por material (producto21)
4. agrupa todo en dos grandes bloques del cuadro: Confecciones y Textiles
5. deja una clasificación macro adicional con grupo3
6. genera las variables monetarias que el Excel necesita
```

La idea más importante de todas es esta:

```python
Textil no se reporta por producto aduanal puro
se reporta por jerarquías de negocio
```

Y esas jerarquías nacen justamente aquí, dentro de `aplicar_transformaciones()`.
