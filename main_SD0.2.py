# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(PV)s
"""

from scipy.stats import gaussian_kde
import pandas as pd
import sys
from utils_16_SD import after_deviant,SD_panel_1_combined,correl_matrix, average_oddball,figure4


pd.options.display.max_columns = None
pd.options.display.max_colwidth = None
pd.options.display.max_rows = None
fign=0

col_types={
    "animal": "string",
    'oddball': 'string',
    'neuron': 'string',
    'unit':'string',
    'division': 'string',
    'animal_unit': 'string',
    'Metadata': 'string'
}

df = pd.read_csv('csvs/oddball_dataset.csv',dtype=col_types)

# This function avoids reclassifying the after-deviant condition each time the program is executed.
def main(df,rall=True):
    columns_to_check = ['animal', 'animal_unit', 'merged_column']

    for column in columns_to_check:
        unique_count = df[column].nunique()
        print(f"La columna '{column}' tiene {unique_count} valores únicos.")
    
    if rall== False:
        dfwad=  pd.read_csv('csvs/odd_data_with_AD.csv')
    else:
        dfodd=df.groupby('animal_unit')
        dfwad= pd.DataFrame()
        for oddball ,group in dfodd:
            df_after_d_group=after_deviant(group)
            dfwad=pd.concat([dfwad,df_after_d_group])
        dfwad.to_csv('csvs/odd_data_with_AD.csv', index=False)
    return dfwad

df2=main(df)#,rall= False rows_with_nan_in_B = df[df['trial'].isna()]
#Panel showing two example neurons.
neuron_list = ['21_023_6-1','21_023_8-1']#,'21_023_9-1'['22_024_2-1','22_033_1-1','22_026_2-1']
SD_panel_1_combined(df2, neuron_list)


correl_matrix(df2)
print(df.oddball.nunique())
#pdf_rasters(df2)

df_av=average_oddball(df2)
print(df_av.shape)
df_for_R = 'csvs/df_aver_with_S_D_AD.csv'

df_av.to_csv(df_for_R, index=False)

figure4(df_av)

sys.exit()

