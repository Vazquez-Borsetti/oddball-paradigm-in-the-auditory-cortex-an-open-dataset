# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(PV)s
"""

import pandas as pd
import re

# Opciones de pandas
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None
pd.options.display.max_rows = None

# Función para extraer números
def extraer_numeros(texto):
    match = re.match(r'^(\d+)-(\d+)-', texto)
    return f"{match.group(1)}-{match.group(2)}" if match else None

# Cargar datos
oddball_data = pd.read_csv('csvpre/data_frame_final_ODD_ach.csv')
unit_table = pd.read_excel('csvpre/Unit_Table_ACh.xlsx')
block_list = pd.read_excel('csvpre/BlockList(final).xlsx')

block_list["animal_unit"] = block_list["tank"] + "_" + block_list["unit"]
# Reorganización de datos en block_list
columns_to_merge = ["control_block_1", "control_block_2", "effect_block_1", "effect_block_2", "rec_block_1", "rec_block_2"]
block_list_long = block_list.melt(id_vars=["tank","animal_unit"], value_vars=columns_to_merge, var_name="block_type", value_name="block_value")
block_list_long['block_value'] = block_list_long['block_value'].str.replace('ASC', 'ODD', regex=True)
block_list_long['block_value'] = block_list_long['block_value'].str.replace('DESC', 'ODD', regex=True)
block_list_long['block_value'] = block_list_long['block_value'].str.replace('DES', 'ODD', regex=True)



# unique_oddball = oddball_data[oddball_data['animal'] == '19_031']['oddball'].unique()
# print(unique_oddball)

oddball_data.loc[oddball_data['oddball'].isin(['3-1-ASC-9-8-F1']), 'oddball'] = '3-1-ASC-8-9-F1'
oddball_data.loc[oddball_data['oddball'].isin(['3-1-ASC-8-9-C1-REPrenamed']), 'oddball'] = '3-1-ASC-8-9-C1-REP'
#print(oddball_data['oddball'].isin(['3-1-ASC-8-9-C1-REP']).any())



oddball_data['oddball'] = oddball_data['oddball'].str.replace('ASC', 'ODD', regex=True)
oddball_data['oddball'] = oddball_data['oddball'].str.replace('DESC', 'ODD', regex=True)
oddball_data['oddball'] = oddball_data['oddball'].str.replace('DES', 'ODD', regex=True)
# Crear columnas combinadas
block_list_long["merged_column"] = block_list_long["tank"] + "_" + block_list_long["block_value"]

oddball_data["merged_column"] = oddball_data["animal"] + "_" + oddball_data["oddball"]

# Filtrar datos y fusionar
oddball_data['unit'] = oddball_data['oddball'].apply(extraer_numeros)
oddball_data['animal_unit'] = oddball_data['animal'] + "_" + oddball_data['unit']
unit_table['ANIMAL_UNIT'] = unit_table['ANIMAL'] + "_" + unit_table['UNIT']
merged_data = pd.merge(oddball_data, unit_table, left_on='animal_unit', right_on='ANIMAL_UNIT', how='left')
#print(merged_data [merged_data['animal'] == '18_175'])

block_list_long = pd.merge(block_list_long, unit_table, left_on='animal_unit', right_on='ANIMAL_UNIT', how='left')

#print(merged_data[merged_data['merged_column'] == '21_016_14-2-ODD-10-9-F1'])
# Filtrar por `merged_column` y agregar información de `block_type`
merged_data = merged_data[merged_data['merged_column'].isin(block_list_long['merged_column'])]
#print(merged_data [merged_data['animal'] == '21_016'].head())
merged_data = merged_data.merge(block_list_long[['merged_column', 'block_type']], on='merged_column', how='left')
# Eliminar datos  específicos
# missing_rows = block_list_long[~block_list_long['merged_column'].isin(merged_data['merged_column'])]
# missing_rows.dropna(axis=0, how='any', subset='merged_column', inplace=True)
#print(missing_rows['merged_column'])
# Concatenar las filas faltantes con filtered_data
# filtered_data = pd.concat([merged_data, missing_rows], ignore_index=True)
# columns_with_nan_in_trial = filtered_data[filtered_data['trial'].isna()]
#print(columns_with_nan_in_trial)
with open("drop.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Une las listas en una sola
combined_list = []
for line in lines:
    
    # Evalúa cada línea como una lista y extiende la lista combinada
    combined_list.extend(eval(line.strip()))

#print(missing_rows)

filtered_data = merged_data[~merged_data['merged_column'].isin(combined_list)]
filtered_data.drop(columns=['ANIMAL_UNIT', 'ANIMAL','UNIT','REMARKS','STATION','path'], inplace=True)
columns_with_nan_in_trial = filtered_data[filtered_data['trial'].isna()]
print(columns_with_nan_in_trial)
# #add metadata 
# # Leer los metadatos desde el archivo
# with open("Metadata.txt", "r") as f:
#     metadata_list = f.read().splitlines()

# # Unir los metadatos en una sola cadena (si son varias líneas)
# metadata_str = " | ".join(metadata_list)

# # Crear una nueva columna 'Metadata' con NaN en todas las filas
# filtered_data["Metadata"] = pd.NA

# # Asignar los metadatos solo en la primera fila
# filtered_data.at[0, "Metadata"] = metadata_str
# Exportar a CSV

filtered_data = filtered_data.rename(columns={'frec': 'freq'})
filtered_data = filtered_data.drop('value', axis=1)
filtered_data = filtered_data.rename(columns={
    'DIVISION': 'division',
    'DEPTH (Z)' : 'depth (Z)',
    'BF (khz)' : 'BF (kHz)',   # conservás la sigla BF
    'TF(dBs)' : 'MT (dB)',    # conservás la sigla TF
    'X (Rostro-Caudal)' : 'rostrocaudal (X)',
    'Y' : 'mediolateral (Y)'

})
filtered_data.to_csv('oddball_dataset.csv', index=False)
# print(filtered_data.groupby('animal_unit')['merged_column'].nunique())
# print('***********')
# print(filtered_data [filtered_data['animal_unit'] == '21_016_8-1'].merged_column.unique())
# print(filtered_data [filtered_data['merged_column'] == '19_120_1-1-ODD-7-8-C1-REP-2'].merged_column.unique())
# print(filtered_data [filtered_data['animal_unit'] == '21_021_6-3'].head())
#print(filtered_data.dropna(subset=['value']))
#print(filtered_data [filtered_data['animal'] == '21_016_14-2'].head())