import pandas as pd
from pathlib import Path

p = Path('c:/Users/gmendoza/Desktop/DDPI-REPOSITORIOS/ddpi/templates/Cuadros de RMC-mar-2026-Joel-act.xlsx')
df = pd.read_excel(p, sheet_name='Indices_M_Textil', header=None)
print('shape', df.shape)
for r in [1, 3, 8, 9, 10]:
    row = df.iloc[r]
    print('\nrow', r+1)
    for idx, val in enumerate(row.tolist()):
        if isinstance(val, str) and val.strip() != '':
            print(idx+1, repr(val))

print('\nrow 11 non-empty first 60 cols:')
row = df.iloc[10]
for idx, val in enumerate(row.tolist()[:120]):
    if pd.notna(val):
        print(idx+1, val)
