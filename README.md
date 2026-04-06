# 📊 Pipeline RMC - Reporte Mensual de Comercio

Automatización integral para el procesamiento, transformación y generación de reportes mensuales de comercio exterior. Sistema modular que integra carga de datos, procesamiento estadístico y exportación automática a plantillas Excel.

## 🎯 Características Principales

- **Carga automatizada** de bases de datos en Excel y formatos Stata
- **Procesamiento completo** con múltiples niveles de agregación
- **Transformaciones de datos** con clasificaciones personalizadas por sector
- **Generación dininámica** de tablas pivote y rankings
- **Exportación a Excel** con poblamiento automático de plantillas
- **Logging detallado** para auditoría y debugging
- **Manejo robusto** de errores con validaciones en cada etapa

## 📋 Requisitos Previos

- Python 3.8+
- Pandas >= 2.0.0
- OpenPyXL >= 3.10.0
- NumPy >= 1.24.0

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/ddpi_rmc.git
cd ddpi_rmc
```

### 2. Crear entorno virtual
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

```
ddpi_rmc/
├── main.py                          # Punto de entrada principal
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
├── pipeline.log                     # Log de ejecuciones (generado)
│
├── data/
│   └── raw/                         # Datos de entrada
│       ├── BD_Expo_*.xlsx           # Base de datos de exportaciones
│       ├── correlac_2022_pais.dta   # Correlaciones país
│       ├── correlac_2022_prod.xlsx  # Correlaciones producto
│       └── correlac_2022_capitulo.dta # Correlaciones capítulo
│
├── outputs/
│   ├── reportes/                    # Reportes generados
│   │   └── RMC_ene_2026.xlsx        # Excel final con datos
│   └── tablas/                      # Tablas intermedias
│
├── templates/
│   └── Cuadros de RMC-ene-2026-Joel-act.xlsx  # Plantilla base
│
└── src/
    ├── __init__.py
    ├── config.py                    # Configuración global
    ├── data_loader.py               # Carga de datos
    ├── processing.py                # Procesamiento inicial
    ├── transformations.py           # Transformaciones de datos
    ├── tables.py                    # Generación de tablas
    ├── indices_generator.py         # Generación de índices
    ├── excel_writer.py              # Escritura en Excel
    └── pipeline.py                  # Orquestador principal
```

## ⚙️ Configuración

Edita `src/config.py` para ajustar parámetros:

```python
# Años a procesar
ANIOS = [2026, 2025]

# Meses (hasta el que se trabaja, a partir del cual se elimina)
MES_NUM = [1, 2]

# Mes actual (nombre corto)
MES_ACTUAL = "ene"

# Rutas (se construyen automáticamente desde BASE_DIR)
DATA_RAW = Path("data/raw")
TEMPLATES = Path("templates")
OUTPUTS = Path("outputs")
```

## 🔄 Flujo del Pipeline

```
1. 📥 CARGA DE DATOS
   ├── Lee BD_Expo_*.xlsx
   ├── Carga correlaciones (3 archivos)
   └── Valida existencia de archivos

2. 🧹 PROCESAMIENTO
   ├── Renombra columnas
   ├── Crea campos derivados (cod_capitulo, cuatro_dig)
   ├── Primera agregación (por variables clave)
   ├── Crea periodos (actual, anterior, últimos 12 meses)
   ├── Segunda agregación (por periodos)
   └── Consolida en tabla final

3. 🔄 TRANSFORMACIONES
   ├── Merge con correlaciones (país, producto, capítulo)
   ├── Calcula producto2, producto21, producto3
   ├── Calcula grupo2, grupo3
   ├── Calcula sector2
   ├── Genera variables monetarias (millones_fob, miles_TM)
   └── Aplica lógica de clasificación por sector

4. 📊 GENERACIÓN DE TABLAS
   ├── Tabla sectorial (nivel sector)
   ├── Tabla de grupos (por sector)
   ├── Tabla de productos (por grupo)
   ├── Ranking de destinos (top 5 países)
   └── Número de destinos únicos

5. 📈 GENERACIÓN DE ÍNDICES
   ├── Índices Agropecuario
   ├── Índices Pesquero
   └── Índices Textil

6. 📤 EXPORTACIÓN A EXCEL
   ├── Carga plantilla base
   ├── Completa hoja Comercio_Agro
   ├── Completa hoja comercio_Pesca
   ├── Completa hojas de índices
   └── Guarda RMC_mes_año.xlsx
```

## 📥 Entrada de Datos Requerida

### Archivos obligatorios en `data/raw/`:

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `BD_Expo_2024-2026_ene.xlsx` | Excel | Base de datos de exportaciones |
| `correlac_2022_pais.dta` | Stata | Mapeo de códigos a nombres de países |
| `correlac_2022_prod.xlsx` | Excel | Mapeo de partidas a productos |
| `correlac_2022_capitulo.dta` | Stata | Mapeo de capítulos a industrias |

### Columnas esperadas en BD_Expo:

```
Subpartida, CPAIDES, AÑO, MES, NDOC, VPESNET, FOB, 
Flujo, 2 digitos, CADU, CVIATRA, 4 digitos, y más...
```

Nota: Se renombran automáticamente a `codigo_partida`, `cod_pais`, `año`, `mes`, etc.

## 📤 Salidas Generadas

### Excel Principal (`outputs/reportes/RMC_ene_2026.xlsx`)

**Hoja: Comercio_Agro**
- Tabla sectorial (FOB y TM)
- Grupos principales (2 grupos top)
- Top 5 destinos
- Número de destinos únicos

**Hoja: comercio_Pesca**
- Misma estructura que Agro
- Datos específicos para Pesquero

**Hojas: Indices_X_Agro, Indices_X_Pesca, Indices_X_Textil**
- Todos los productos (ordenados por FOB/TM)
- Top 3 subproductos por grupo
- Clasificaciones detalladas

### Log de Ejecución (`pipeline.log`)

```
2026-03-31 10:45:23 - src.pipeline - INFO - INICIANDO PIPELINE
2026-03-31 10:45:24 - src.data_loader - INFO - Cargando archivo...
2026-03-31 10:45:25 - src.processing - INFO - Procesamiento completado
...
2026-03-31 10:45:35 - src.pipeline - INFO - PIPELINE COMPLETADO EXITOSAMENTE
```

## 🏃 Uso

### Ejecución Simple

```bash
python main.py
```

### Ejecución desde Python

```python
from src.pipeline import run_pipeline
import src.config as config

df_final = run_pipeline()
print(f"Procesados {len(df_final)} registros")
```

### Con variables personalizadas

```python
from pathlib import Path
import src.config as config

# Cambiar mes
config.MES_ACTUAL = "feb"
config.MES_NUM = [2, 3]
config.ANIOS = [2026, 2025]

from src.pipeline import run_pipeline
run_pipeline()
```

## 🔍 Validaciones y Errores

### Validaciones Automáticas

- ✅ Verifica existencia de archivos de entrada
- ✅ Valida tipos de datos (convierte a int, str, float)
- ✅ Maneja valores nulos correctamente
- ✅ Valida existencia de plantilla Excel
- ✅ Crea carpetas de output si no existen

### Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `FileNotFoundError: data/raw/BD_Expo_*.xlsx` | Archivo no existe | Verificar nombre exacto y ruta de archivo |
| `KeyError: 'CPAIDES'` | Columna no encuentra en Excel | Revisar nombres de columnas en fuente |
| `ModuleNotFoundError: No module named 'pandas'` | Dependencia no instalada | Ejecutar `pip install -r requirements.txt` |
| `FileNotFoundError: templates/Cuadros de RMC*` | Plantilla Excel no existe | Verificar nombre y ubicación de plantilla |

## 📊 Métricas de Procesamiento

El pipeline registra automáticamente:

- Cantidad de registros en cada etapa
- Número de períodos procesados
- Tiempo de ejecución (en logs)
- Sectores, grupos y productos únicos
- Número de destinos por período
- Errores y advertencias

## 🧪 Testing

Para validar la instalación:

```bash
# Ver versión de dependencias
pip list | grep -E "pandas|openpyxl|numpy"

# Ejecutar pipeline de test (si existe)
python -m pytest tests/ -v
```

## 📚 Variables Principales Generadas

Durante la ejecución se crean:

| Variable | Descripción |
|----------|-------------|
| `cod_capitulo` | Primeros 2 dígitos de partida |
| `cuatro_dig` | Primeros 4 dígitos de partida |
| `cinco_dig` | Primeros 5 dígitos de partida |
| `millones_fob` | FOB convertido a millones |
| `miles_TM` | Peso neto convertido a miles |
| `producto2` | Clasificación refinada del producto |
| `producto21` | Clasificación adicional (pesquero/textil) |
| `producto3` | Clasificación de familia textil |
| `grupo2` | Agrupación principal |
| `grupo3` | Agrupación detallada |
| `sector2` | Agrupación amplia de sectores |

## 🔗 Períodos Generados

Para mes actual "ene":

```python
periodos = [
    "2025",                  # Año anterior completo
    "Ene 25",               # Enero del año anterior
    "Ene 26",               # Enero del año actual
    "Ult_12_meses"          # Últimos 12 meses
]
```

## 📝 Logging

Todos los eventos se registran en `pipeline.log`:

```bash
# Ver últimas 50 líneas del log
tail -50 pipeline.log

# Filtrar solo errores
grep "ERROR" pipeline.log

# Ver timeline de ejecución
grep "INFO" pipeline.log | grep -E "Cargando|Procesamiento|Transformaciones|Exportando"
```

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia Todos los derechos reservados - DDPI 2026

## 👨‍💻 Autor

**Departamento de Datos para la Integración (DDPI)**

## 📞 Soporte

Para reportar bugs o solicitar features, por favor abre un issue en el repositorio.

## 🔧 Roadmap

- [ ] Soporte para múltiples meses en una sola ejecución
- [ ] Generación de gráficos automáticos
- [ ] Exportación a PDF
- [ ] Dashboard interactivo con Streamlit
- [ ] API REST para consultas dinámicas
- [ ] Tests unitarios completos

## ✨ Changelog

### v1.0.0 (2026-03-31)
- 🎉 Release inicial
- ✅ Pipeline completo de procesamiento
- ✅ Exportación a Excel con múltiples hojas
- ✅ Logging detallado
- ✅ Manejo robusto de errores

---

**Última actualización**: 31 de marzo de 2026
