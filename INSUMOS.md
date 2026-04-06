# 📥 Insumos Requeridos - Pipeline RMC

Guía completa de qué archivos necesitas y cómo deben estar organizados.

## 📋 Resumen Rápido

| Archivo | Ubicación | Formato | Obligatorio |
|---------|-----------|---------|-------------|
| `BD_Expo_2024-2026_ene.xlsx` | `data/raw/` | Excel | ✅ SÍ |
| `correlac_2022_pais.dta` | `data/raw/` | Stata | ✅ SÍ |
| `correlac_2022_prod.xlsx` | `data/raw/` | Excel | ✅ SÍ |
| `correlac_2022_capitulo.dta` | `data/raw/` | Stata | ✅ SÍ |
| `Cuadros de RMC-ene-2026-Joel-act.xlsx` | `templates/` | Excel | ✅ SÍ |

---

## 1️⃣ Base de Datos Principal de Exportaciones

### Nombre exacto:
```
BD_Expo_2024-2026_ene.xlsx
```

**Ubicación:**
```
data/raw/BD_Expo_2024-2026_ene.xlsx
```

### Estructura requerida:

| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| **Subpartida** | Texto | Código de partida (10 dígitos) | `0702000000` |
| **CPAIDES** | Texto | Código de país (3 dígitos) | `051` |
| **AÑO** | Número | Año de la transacción | `2026` |
| **MES** | Número | Mes de la transacción (1-12) | `1` |
| **NDOC** | Texto | Número de documento RUC | `20123456789` |
| **VPESNET** | Número | Peso neto en kg | `15000` |
| **FOB** | Número | Valor FOB en dólares | `45000.50` |
| **Flujo** | Texto | Tipo de flujo | `EXPORTACION` |
| **2 digitos** | Texto | Primeros 2 dígitos de partida | `07` |
| **4 digitos** | Texto | Primeros 4 dígitos de partida | `0702` |
| **CADU** | Texto | Código CADU | `ABC123` |
| **CVIATRA** | Texto | Código de vía de transporte | `01` |

### ⚠️ IMPORTANTE:
- Debe tener al menos **2 años** de datos (2025 y 2026 en el ejemplo)
- Todos los campos **deben estar presentes**, aunque algunos pueden estar vacíos
- Usar formato Excel estándar (`.xlsx`)
- **NO usar** valores nulos sin manejo especial

**Ejemplo de primeras filas:**
```
Subpartida | CPAIDES | AÑO | MES | NDOC | VPESNET | FOB | Flujo | 2 digitos | 4 digitos
0702000000 | 051 | 2025 | 6 | 20123456789 | 5000 | 12500.00 | EXPORTACION | 07 | 0702
0702000000 | 070 | 2026 | 1 | 20987654321 | 3500 | 8750.25 | EXPORTACION | 07 | 0702
```

---

## 2️⃣ Correlacionador de Países

### Nombre exacto:
```
correlac_2022_pais.dta
```

**Ubicación:**
```
data/raw/correlac_2022_pais.dta
```

### Estructura requerida:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| **cod_pais** | Texto | Código de país (3 dígitos) |
| **Pais** | Texto | Nombre del país |
| **Pais_UE27** | Texto | Clasificación UE (usado en destinos) |

### ⚠️ IMPORTANTE:
- Archivo en formato **Stata (.dta)** - NO Excel
- Debe contener mapeo de todos los códigos de país que aparezcan en BD_Expo
- Se usa para enriquecer los datos con nombres legibles

**Ejemplo de contenido:**
```
cod_pais | Pais | Pais_UE27
051 | Filipinas | ASIA
070 | Indonesia | ASIA
110 | Bangladesh | ASIA
156 | China | ASIA
842 | Estados Unidos | OTROS
```

---

## 3️⃣ Correlacionador de Productos

### Nombre exacto:
```
correlac_2022_prod.xlsx
```

**Ubicación:**
```
data/raw/correlac_2022_prod.xlsx
```

### Estructura requerida:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| **codigo_partida** | Texto | Código de partida (10 dígitos) |
| **cuatro_dig** | Texto | Primeros 4 dígitos |
| **Producto** | Texto | Nombre del producto |
| **Familia_Textil** | Texto | Familia si es textil (opcional) |
| **Material_Textil** | Texto | Material si es textil (opcional) |
| **Rubro_Textil** | Texto | Rubro si es textil (opcional) |
| **Sector** | Texto | Sector económico |
| **Grupo** | Texto | Grupo dentro del sector |
| **Clasific_pesquero** | Texto | Clasificación si es pesquero (opcional) |

### ⚠️ IMPORTANTE:
- Archivo en **Excel (.xlsx)**
- Columnas con "Textil" son opcionales si no hay datos textiles
- Columnas con "pesquero" son opcionales si no hay datos de pesca
- Debe mapear TODOS los códigos de partida de BD_Expo

**Ejemplo de contenido:**
```
codigo_partida | cuatro_dig | Producto | Sector | Grupo | Familia_Textil | Material_Textil | Clasific_pesquero
0702000000 | 0702 | Tomate | Agropecuario | Hortalizas | | | 
0703101000 | 0703 | Cebolla | Agropecuario | Hortalizas | | | 
0306169000 | 0306 | Langostino | Pesquero | Langostino | | | Crustáceos
6204620000 | 6204 | Pantalón de mujer | Textil | Confecciones | Prendas de vestir | Algodón | 
```

---

## 4️⃣ Correlacionador de Capítulos

### Nombre exacto:
```
correlac_2022_capitulo.dta
```

**Ubicación:**
```
data/raw/correlac_2022_capitulo.dta
```

### Estructura requerida:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| **cuatro_dig** | Texto | Primeros 4 dígitos de partida |
| **Industria_acero** | Texto | Clasificación de acero si aplica |
| *Otras columnas* | - | Según necesidad de clasificación |

### ⚠️ IMPORTANTE:
- Archivo en formato **Stata (.dta)**
- Principalmente usado para industria siderúrgica y metalúrgica
- Se une con la base sobre el campo `cuatro_dig`

**Ejemplo de contenido:**
```
cuatro_dig | Industria_acero | Clasificacion
7201 | Acero plano | Siderúrgico
7202 | Acero largo | Siderúrgico
7203 | Acero plano | Siderúrgico
7204 | Chatarra | Siderúrgico
```

---

## 5️⃣ Plantilla Excel para Reporte

### Nombre exacto:
```
Cuadros de RMC-ene-2026-Joel-act.xlsx
```

**Ubicación:**
```
templates/Cuadros de RMC-ene-2026-Joel-act.xlsx
```

### Estructura requerida - Hojas:

#### **Hoja 1: Comercio_Agro**
```
Filas a completar automáticamente:
- Fila 10: Datos sectoriales (FOB y TM)
- Filas 11-41: Grupos principales (hasta 2 grupos)
- Filas 55-59: Top 5 destinos
- Fila 62: Número de destinos
```

#### **Hoja 2: comercio_Pesca**
```
Filas a completar automáticamente:
- Fila 10: Datos sectoriales
- Filas 37-40: Top 4 destinos
- Fila 41: Número de destinos
```

#### **Hoja 3: Indices_X_Agro**
```
Columnas a completar:
- Columna A: Código de partida (TM del sector)
- Columnas B-D: Períodos (TM)
- Columna H: Código de partida (FOB del sector)
- Columnas I-K: Períodos (FOB)
- [Más columnas para otros índices]
```

#### **Hoja 4: Indices_X_Pesca**
```
Misma estructura que Agro
```

#### **Hoja 5: Indices_X_Textil**
```
Misma estructura que Agro
```

### ⚠️ IMPORTANTE:
- Plantilla debe tener **exactamente estos nombres de hojas**
- Las columnas deben tener encabezados en fila 10
- El pipeline escribirá SOBRE datos existentes (sobrescribe)
- Debe estar en **Excel (.xlsx)**

---

## 📂 Estructura de Carpetas Necesaria

```
ddpi_rmc/
│
├── data/
│   └── raw/
│       ├── BD_Expo_2024-2026_ene.xlsx           ✅ OBLIGATORIO
│       ├── correlac_2022_pais.dta               ✅ OBLIGATORIO
│       ├── correlac_2022_prod.xlsx              ✅ OBLIGATORIO
│       └── correlac_2022_capitulo.dta           ✅ OBLIGATORIO
│
├── templates/
│   └── Cuadros de RMC-ene-2026-Joel-act.xlsx    ✅ OBLIGATORIO
│
└── outputs/
    ├── reportes/                                (se crea automáticamente)
    └── tablas/                                  (se crea automáticamente)
```

---

## 🔄 Cambiar Mes y Año

Si quieres procesar un mes diferente, **debes cambiar:**

1. **En `src/config.py`:**
```python
MES_ACTUAL = "feb"  # cambiar a febrero
MES_NUM = [2, 3]    # trabaja hasta febrero, elimina marzo
ANIOS = [2026, 2025]
```

2. **En nombre de archivo BD_Expo:**
```
BD_Expo_2024-2026_feb.xlsx  # cambiar extensión
```

3. **En nombre de archivo de template:**
```
Cuadros de RMC-feb-2026-Joel-act.xlsx  # cambiar mes
```

4. **En nombre de output (automático):**
```
RMC_feb_2026.xlsx  # se genera automáticamente
```

---

## ✅ Checklist Antes de Ejecutar

- [ ] Carpeta `data/raw/` existe y contiene 4 archivos requeridos
- [ ] Carpeta `templates/` existe y contiene plantilla Excel
- [ ] `BD_Expo_*.xlsx` tiene todas las columnas requeridas
- [ ] Archivos `.dta` están en formato Stata (no convertidos a Excel)
- [ ] Nombres de archivos coinciden exactamente (incluyendo mayúsculas/minúsculas)
- [ ] Los códigos en BD_Expo existen en los correlacionadores
- [ ] Plantilla Excel tiene exactos nombres de hojas
- [ ] Las carpetas `outputs/reportes` y `outputs/tablas` existen (o se crearán)
- [ ] Archivo `requirements.txt` instalado

---

## 🆘 Troubleshooting por Archivo

### BD_Expo_*.xlsx
**Error:** `FileNotFoundError: BD_Expo_2024-2026_ene.xlsx`
- **Solución:** Verificar nombre exacto, no debería haber espacios extras ni diferencias en mayúsculas

**Error:** `KeyError: 'CPAIDES'` o similar
- **Solución:** Columna no existe. Verificar nombres exactos en Excel

**Error:** `ValueError: unable to parse string`
- **Solución:** Hay valores en formato incorrecto (ej: "ABC" en columna numérica)

### correlac_2022_pais.dta
**Error:** `UnicodeDecodeError` o lectura incorrecta
- **Solución:** Asegurar que es formato Stata `.dta`, no convertido a Excel

### correlac_2022_prod.xlsx
**Error:** Muchos NaN después del merge
- **Solución:** Hay códigos en BD_Expo que no están en correlacionador. Agregar registros faltantes

### Plantilla Excel
**Error:** `ValueError: worksheet 'Comercio_Agro' not found`
- **Solución:** Verificar nombres exactos de hojas (sensible a mayúsculas y espacios)

---

## 📝 Notas Importantes

1. **Encoding:** Asegurar que archivos Excel usan encoding UTF-8
2. **Números:** Las columnas numéricas deben ser números, no texto
3. **Fechas:** Usar formato numérico para años/meses (no fechas formateadas)
4. **Nombres duplicados:** Evitar espacios al final de textos
5. **Correlacionadores:** Deben tener cobertura del 100% de códigos únicos en BD_Expo
6. **Actualización mensual:** Solo cambiar el mes en config.py y en nombres de archivos

---

**Última actualización:** 31 de marzo de 2026
