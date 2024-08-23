import os
import pandas as pd
from importtdt05b import data_estractor
import sys
import re
lista_dataframes = []
def buscar_subdirectorios(directorio_raiz):
    patron = re.compile(r'\b[1-9]-[1-9]-.*ODD.*[1-9]-[1-9]-C.*\b')

    subdirectorios_coincidentes = []

    for root, dirs, files in os.walk(directorio_raiz):
        for dir_name in dirs:
            ruta= os.path.join(root,dir_name)
            if patron.match(dir_name):
                #grupo1, grupo2, grupo3, grupo4 = patron.match(dir_name).groups()
                print (dir_name[2])
                print (ruta)

                df=data_estractor(ruta)
                df['animal']=os.path.basename(root)
                df['oddball']=dir_name
                df['tract']= dir_name[0]
                df['neuron']= dir_name[2]
                lista_dataframes.append(df)
                #subdirectorios_coincidentes.append(ruta)


    #return subdirectorios_coincidentes
directorio_raiz = "electro/TANKS/"#
subdirectorios_coincidentes = buscar_subdirectorios(directorio_raiz)
data_frame_final = pd.concat(lista_dataframes, ignore_index=True)
print(data_frame_final['animal'].nunique())
#selected_rows = data_frame_final[data_frame_final['oddbal'] == '1-1-ODD-7-8-C1']
#print (selected_rows.sample(40))
data_frame_final.to_csv('data_frame_final_ODD.csv',index=False)
sys.exit()
# Ejemplo de uso


#print(name for name in os.listdir(directorio_raiz ))
print("Subdirectorios coincidentes:")
for subdirectorio in subdirectorios_coincidentes:
    print(subdirectorio)


# Ruta de la carpeta que contiene los archivos CSV
ruta_carpeta = 'neurons'


data_frame_final = pd.concat(lista_dataframes, ignore_index=True)
print (data_frame_final.sample(20))
data_frame_final.to_csv('data_frame_final.csv',index=False)
