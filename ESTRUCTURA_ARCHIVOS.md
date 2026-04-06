# 📁 Estructura de Archivos - Guía Visual

## 🎯 Estructura Completa del Proyecto

```
ddpi_rmc/
│
├─ 📄 main.py                          ← Ejecutar esto: python main.py
├─ 📄 README.md                        ← Documentación general
├─ 📄 INSUMOS.md                       ← Este documento
├─ 📄 requirements.txt                 ← Dependencias Python
├─ 📄 pipeline.log                     ← Se genera automáticamente
│
├─ 📂 data/                            ← CARPETA DE ENTRADA
│  └─ 📂 raw/                          ← Aquí van tus 4 archivos
│     ├─ 📊 BD_Expo_2024-2026_ene.xlsx        ✅ OBLIGATORIO
│     ├─ 📊 correlac_2022_pais.dta            ✅ OBLIGATORIO
│     ├─ 📊 correlac_2022_prod.xlsx           ✅ OBLIGATORIO
│     └─ 📊 correlac_2022_capitulo.dta        ✅ OBLIGATORIO
│
├─ 📂 templates/                       ← CARPETA DE PLANTILLAS
│  └─ 📊 Cuadros de RMC-ene-2026-Joel-act.xlsx  ✅ OBLIGATORIO
│
├─ 📂 outputs/                         ← CARPETA DE SALIDA (se crea sola)
│  ├─ 📂 reportes/                     ← Reportes finales
│  │  └─ 📊 RMC_ene_2026.xlsx          ← Se genera aquí
│  └─ 📂 tablas/                       ← Tablas intermedias
│
└─ 📂 src/                             ← CÓDIGO MODULAR
   ├─ 📄 __init__.py
   ├─ 📄 config.py                    ← Configuración global
   ├─ 📄 data_loader.py               ← Carga archivos
   ├─ 📄 processing.py                ← Procesa datos
   ├─ 📄 transformations.py           ← Transforma datos
   ├─ 📄 tables.py                    ← Genera tablas
   ├─ 📄 indices_generator.py         ← Genera índices
   ├─ 📄 excel_writer.py              ← Escribe en Excel
   └─ 📄 pipeline.py                  ← Orquestador principal
```

## ✅ Checklist de Archivos

### ANTES de ejecutar python main.py:

```
┌─────────────────────────────────────────────────────────┐
│ CARPETA: data/raw/                                      │
├─────────────────────────────────────────────────────────┤
│ ☐ BD_Expo_2024-2026_ene.xlsx        (formato: .xlsx)   │
│   └─ Contenido: Datos de exportaciones                  │
│   └─ Tamaño típico: 50-500 MB                           │
│                                                         │
│ ☐ correlac_2022_pais.dta            (formato: .dta)    │
│   └─ Contenido: Mapeo país (cod → nombre)              │
│   └─ Tamaño típico: < 1 MB                             │
│                                                         │
│ ☐ correlac_2022_prod.xlsx           (formato: .xlsx)   │
│   └─ Contenido: Mapeo productos (partida → nombre)     │
│   └─ Tamaño típico: 5-50 MB                            │
│                                                         │
│ ☐ correlac_2022_capitulo.dta        (formato: .dta)    │
│   └─ Contenido: Mapeo capítulos (industria)            │
│   └─ Tamaño típico: < 1 MB                             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ CARPETA: templates/                                     │
├─────────────────────────────────────────────────────────┤
│ ☐ Cuadros de RMC-ene-2026-Joel-act.xlsx (formato: .xlsx)
│   └─ Hojas: Comercio_Agro, comercio_Pesca,             │
│              Indices_X_Agro, Indices_X_Pesca,          │
│              Indices_X_Textil                          │
│   └─ Tamaño típico: 1-5 MB                             │
└─────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Archivos Durante Ejecución

```
ENTRADA (data/raw/)
    │
    ├─→ BD_Expo_2024-2026_ene.xlsx
    │       ↓ (data_loader.py)
    │    DataFrame 1 (base cruda)
    │       ↓ (processing.py)
    │    DataFrame 2 (procesado)
    │       ↓ (transformations.py)
    │    DataFrame 3 (transformado)
    │       ↓ (tables.py)
    │    Tabla final + Rankings
    │       ↓ (indices_generator.py)
    │    Índices sectoriales
    │       ↓ (excel_writer.py + templates/)
    │
    ├─→ correlac_2022_pais.dta
    │       ↓ (merge en transformations.py)
    │    Datos enriquecidos
    │
    ├─→ correlac_2022_prod.xlsx
    │       ↓ (merge en transformations.py)
    │    Datos enriquecidos
    │
    ├─→ correlac_2022_capitulo.dta
    │       ↓ (merge en transformations.py)
    │    Datos enriquecidos
    │
    └─→ templates/Cuadros de RMC-ene-2026...xlsx
            ↓ (copia + sobrescribe)

SALIDA (outputs/reportes/)
    └─→ RMC_ene_2026.xlsx ✅
```

## 📊 Columnas Esperadas en Cada Archivo

### BD_Expo_2024-2026_ene.xlsx
```
┌──────────────┬─────────┬───────────────────────────┐
│ Columna      │ Tipo    │ Ejemplo                   │
├──────────────┼─────────┼───────────────────────────┤
│ Subpartida   │ Texto   │ 0702000000                │
│ CPAIDES      │ Texto   │ 051                       │
│ AÑO          │ Número  │ 2026                      │
│ MES          │ Número  │ 1                         │
│ NDOC         │ Texto   │ 20123456789               │
│ VPESNET      │ Número  │ 15000                     │
│ FOB          │ Número  │ 45000.50                  │
│ Flujo        │ Texto   │ EXPORTACION               │
│ 2 digitos    │ Texto   │ 07                        │
│ 4 digitos    │ Texto   │ 0702                      │
│ CADU         │ Texto   │ ABC123                    │
│ CVIATRA      │ Texto   │ 01                        │
│ Producto     │ Texto   │ Tomate                    │
│ Sector       │ Texto   │ Agropecuario              │
│ Grupo        │ Texto   │ Hortalizas                │
└──────────────┴─────────┴───────────────────────────┘
```

### correlac_2022_pais.dta
```
┌────────────┬──────────────────────────┐
│ cod_pais   │ Pais        │ Pais_UE27  │
├────────────┼──────────────┼────────────┤
│ 051        │ Filipinas   │ ASIA       │
│ 070        │ Indonesia   │ ASIA       │
│ 156        │ China       │ ASIA       │
│ 842        │ EEUU        │ OTROS      │
└────────────┴──────────────┴────────────┘
```

### correlac_2022_prod.xlsx
```
┌────────────────┬────────────┬──────────────┬────────────┐
│ codigo_partida │ cuatro_dig │ Producto     │ Sector     │
├────────────────┼────────────┼──────────────┼────────────┤
│ 0702000000     │ 0702       │ Tomate       │ Agro       │
│ 0306169000     │ 0306       │ Langostino   │ Pesquero   │
│ 6204620000     │ 6204       │ Pantalón     │ Textil     │
└────────────────┴────────────┴──────────────┴────────────┘
```

### correlac_2022_capitulo.dta
```
┌────────────┬──────────────────┐
│ cuatro_dig │ Industria_acero  │
├────────────┼──────────────────┤
│ 7201       │ Acero plano      │
│ 7202       │ Acero largo      │
│ 7204       │ Chatarra         │
└────────────┴──────────────────┘
```

## 🎯 Actualización Mensual

Cada mes debes cambiar:

```diff
Mes: ENERO
─────────────────────────────────────────
- Archivo: BD_Expo_2024-2026_ene.xlsx
- Template: Cuadros de RMC-ene-2026-Joel-act.xlsx
- config.py: MES_ACTUAL = "ene"
- Output: RMC_ene_2026.xlsx

↓ (Para siguiente mes)

Mes: FEBRERO
─────────────────────────────────────────
+ Archivo: BD_Expo_2024-2026_feb.xlsx  🔄 CAMBIAR
+ Template: Cuadros de RMC-feb-2026-Joel-act.xlsx  🔄 CAMBIAR
+ config.py: MES_ACTUAL = "feb"  🔄 CAMBIAR
  config: MES_NUM = [2, 3]  🔄 CAMBIAR
- Output: RMC_feb_2026.xlsx (automático)
```

## 🚀 Primer Uso - Paso a Paso

### 1. Crear carpeta data/raw/ con archivos
```powershell
# En Windows PowerShell
cd ddpi_rmc
mkdir data\raw  # Si no existe
# Copiar 4 archivos aquí
```

### 2. Crear carpeta templates/ con plantilla
```powershell
mkdir templates  # Si no existe
# Copiar plantilla Excel aquí
```

### 3. Verificar estructura
```powershell
tree /F  # Ver estructura completa
```

### 4. Ejecutar pipeline
```powershell
python main.py
```

### 5. Verificar salida
```powershell
# Debe existir:
# outputs/reportes/RMC_ene_2026.xlsx
# pipeline.log
```

## 📋 Errores Comunes y Soluciones

| Síntoma | Causa | Solución |
|---------|-------|----------|
| `FileNotFoundError: data/raw/BD_Expo...` | Archivo no existe o mal nombrado | Copiar archivo con nombre **exacto** |
| `UnicodeDecodeError` con archivos .dta | Archivo .dta corrompido | Reconvertir desde formato original |
| `KeyError: 'CPAIDES'` | Columna no existe en Excel | Verificar nombres de columnas exactos |
| `worksheet ... not found` | Hoja Excel no existe | Verificar nombres de hojas exactos |
| `ValueError: unable to parse` | Formato incorrecto en celda | Limpiar datos, convertir a tipo correcto |

## 🔗 Relaciones Entre Archivos

```
BD_Expo_2024-2026_ene.xlsx
    │
    ├─→ [Subpartida] 
    │       ↓ (merge)
    │   correlac_2022_prod.xlsx [codigo_partida]
    │       ↓
    │   Agrega: Producto, Sector, Grupo, Familia_Textil...
    │
    └─→ [CPAIDES] 
            ↓ (merge)
        correlac_2022_pais.dta [cod_pais]
            ↓
        Agrega: Pais, Pais_UE27
        
┌─────────────────────────────────────┐
│ También usa:                        │
│ - correlac_2022_capitulo.dta        │
│   (merge en cuatro_dig)             │
└─────────────────────────────────────┘
```

---

**Última actualización:** 31 de marzo de 2026
