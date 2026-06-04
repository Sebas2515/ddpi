import pandas as pd
from pathlib import Path

p = Path(r'c:/Users/gmendoza/Desktop/DDPI-REPOSITORIOS/ddpi/data/raw/BD_Impo_2025-2026_abr.xlsx')
print('path exists:', p.exists())

xl = pd.ExcelFile(p)
print('sheet_names:', xl.sheet_names)

df = pd.read_excel(p, sheet_name=0)
print('columns:', list(df.columns))

for col in ['Material_Textil', 'Familia_Textil', 'Producto', 'Grupo', 'Rubro_Textil']:
    if col in df.columns:
        vals = df[col].dropna().astype(str).unique()
        print(f'--- {col} ({len(vals)}) ---')
        print(vals[:50])

if 'Material_Textil' in df.columns:
    pol = [val for val in df['Material_Textil'].dropna().astype(str).unique() if 'poli' in val.lower()]
    print('--- Poliester check ---')
    print(pol[:50])
