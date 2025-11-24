# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(PV)s
"""
import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None
pd.options.display.max_rows = None
df = pd.read_csv('csvs/oddball_dataset.csv')
df1=pd.read_csv('csvs/df_aver_with_S_D_AD.csv')
df2=pd.read_csv('csvs/odd_data_with_AD.csv')
print (df1.sample(20))
#filas_con_nan = df[df['freq'].isna()]
# df_filtrado = df[df['animal'] == '22_020']
# df_filtrado = df_filtrado[df_filtrado['oddball'] == '1-2-ODD-9-10-C1']
# print(df_filtrado.sample(30))