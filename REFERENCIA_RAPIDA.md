# ⚡ Referencia Rápida de Insumos

## 📦 Los 4 Archivos Que NECESITAS

### 1. Base de Datos Excel
```
📊 BD_Expo_2024-2026_ene.xlsx
   Ubicación: data/raw/
   Tamaño: 50-500 MB
   ✓ Columnas mínimas:
     - Subpartida, CPAIDES, AÑO, MES
     - NDOC, VPESNET, FOB, Flujo
     - 2 digitos, 4 digitos, CADU, CVIATRA
```

### 2. Correlacionador País (Stata)
```
📊 correlac_2022_pais.dta
   Ubicación: data/raw/
   Tamaño: < 1 MB
   ✓ Columnas:
     - cod_pais (texto)
     - Pais (nombre país)
     - Pais_UE27 (clasificación)
```

### 3. Correlacionador Producto (Excel)
```
📊 correlac_2022_prod.xlsx
   Ubicación: data/raw/
   Tamaño: 5-50 MB
   ✓ Columnas:
     - codigo_partida
     - cuatro_dig
     - Producto, Sector, Grupo
     - (Opcional: Familia_Textil, Material_Textil, etc)
```

### 4. Correlacionador Capítulo (Stata)
```
📊 correlac_2022_capitulo.dta
   Ubicación: data/raw/
   Tamaño: < 1 MB
   ✓ Columnas:
     - cuatro_dig
     - Industria_acero (o similares)
```

## 🎯 La Plantilla Excel

```
📊 Cuadros de RMC-ene-2026-Joel-act.xlsx
   Ubicación: templates/
   ✓ Hojas requeridas:
     1. Comercio_Agro
     2. comercio_Pesca
     3. Indices_X_Agro
     4. Indices_X_Pesca
     5. Indices_X_Textil
```

## 📂 Estructura Mínima

```
ddpi_rmc/
├─ data/raw/  ← Aquí van los 4 archivos
├─ templates/ ← Aquí va la plantilla
├─ src/       (ya está)
└─ main.py    (ya está)
```

## ✅ Pre-Checklist (5 segundos)

```
☐ Existen 4 archivos en data/raw/
☐ Existe plantilla en templates/
☐ Nombres coinciden exactamente
☐ Archivos .dta están en Stata (no convertidos)
☐ Archivos .xlsx están en Excel
```

## 🎯 Para Cambiar de Mes

Solo 3 cambios:
```
1. Cambiar BD_Expo_*_ene.xlsx → BD_Expo_*_feb.xlsx
2. Cambiar plantilla ene → feb en templates/
3. En src/config.py:
   MES_ACTUAL = "feb"
   MES_NUM = [2, 3]
```

## 🚀 Ejecutar

```powershell
python main.py
```

**Salida:**
- `outputs/reportes/RMC_ene_2026.xlsx` ← El reporte final
- `pipeline.log` ← Log de ejecución

---

**¿Dudas?** Ver INSUMOS.md o ESTRUCTURA_ARCHIVOS.md

**Última actualización:** 31 de marzo de 2026
