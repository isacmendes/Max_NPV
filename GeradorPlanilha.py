import pandas as pd
import openpyxl

#df = pd.DataFrame({'A': range(10), 'B': range(11, 21, 1)})
df = pd.DataFrame(columns=['A', 'B'])

for linha in range(10):
    df.loc[linha] = [linha + 1, linha + 2]

df.to_excel('planilha.xlsx', sheet_name='plan1', engine='openpyxl', index=False)