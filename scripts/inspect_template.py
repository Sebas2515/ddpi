import pandas as pd
from pathlib import Path

p = Path(r"c:\Users\gmendoza\Desktop\DDPI-REPOSITORIOS\ddpi\templates\Cuadros de RMC-abr-2026-Joel-act.xlsx")
print('PATH', p)

xls = pd.ExcelFile(p)
print('Sheets:', xls.sheet_names)

for sheet in ['Comercio_Textil', 'Hoja1', 'comercio 13 paises', 'Indices_X_Textil', 'Indices_M_Textil']:
    if sheet not in xls.sheet_names:
        continue
    df = pd.read_excel(p, sheet_name=sheet, header=None)
    print('\nSHEET', sheet, 'shape', df.shape)
    if sheet == 'Comercio_Textil':
        for i in range(df.shape[0]):
            row = df.iloc[i].astype(str).fillna('')
            row_text = ' | '.join(str(x) for x in row.tolist())
            if any(key in row_text.lower() for key in ['hilos', 'hilados', 'poliester', 'poliéster', 'algodon', 'algodón', 'tejidos', 'textiles']):
                print('ROW', i, row_text)
        print('\n--- CONTEXTO FILAS 8-55 ---')
        for i in range(8, min(56, df.shape[0])):
            row = df.iloc[i].astype(str).fillna('')
            row_text = ' | '.join(str(x).strip() for x in row.tolist())
            if any('hilos' in row_text.lower() or 'tejidos' in row_text.lower() or 'poliester' in row_text.lower() or 'confeccion' in row_text.lower() or 'textiles' in row_text.lower() for x in [row_text]):
                print('CTX', i, row_text)
