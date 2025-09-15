import os
import pandas as pd
import matplotlib.pyplot as plt
from importtdt07 import data_estractor
import sys
import re

lista_dataframes = []
errors = []  # Inicializa la lista para almacenar errores

def buscar_subdirectorios(directorio_raiz):
    patron = re.compile(r'\b[1-9][0-9]?-[1-9][0-9]?-.*\b(ODD|ASC|DESC).*')  # Patrón de subdirectorios

    for root, dirs, files in os.walk(directorio_raiz):
        for dir_name in dirs:
            ruta = os.path.join(root, dir_name)
            if patron.match(dir_name):
                print(f"Procesando subdirectorio: {dir_name}")
                try:
                    df = data_estractor(ruta)
                    
                    # Si `df` es válido y no está vacío
                    #if df is not None and not df.empty:
                    df['animal'] = os.path.basename(root)
                    df['oddball'] = dir_name
                    df['tract'] = dir_name[0]
                    df['neuron'] = dir_name[2]
                    df['path'] = os.path.relpath(ruta, directorio_raiz)  # Ruta relativa
                    lista_dataframes.append(df)
                    # else:
                    #     # Si `df` es vacío, agregar datos con ceros
                    #     print(f"Datos vacíos en {ruta}. Agregando fila con ceros.")
                    #     df_vacio = pd.DataFrame([{
                    #         'animal': os.path.basename(root),
                    #         'oddball': dir_name,
                    #         'tract': dir_name[0],
                    #         'neuron': dir_name[2],
                    #         'path': os.path.relpath(ruta, directorio_raiz),  # Ruta relativa
                    #         'value': 1  # Agrega más columnas si es necesario
                    #     }])
                        #lista_dataframes.append(df_vacio)
                    
                except Exception as e:
                    # Captura cualquier error que ocurra en la función data_estractor
                    error_message = f"Error procesando {ruta}: {str(e)}"
                    errors.append(error_message)
                    print(error_message)
                    print('*******88888888******')
                    
                    # # Agrega una fila con ceros para mantener consistencia
                    # df_error = pd.DataFrame([{
                    #     'animal': os.path.basename(root),
                    #     'oddball': dir_name,
                    #     'tract': dir_name[0],
                    #     'neuron': dir_name[2],
                    #     'path': os.path.relpath(ruta, directorio_raiz),
                    #     'value': 1 # Otras columnas según sea necesario
                    # }])
                    # lista_dataframes.append(df_error)

# Ruta del directorio raíz
directorio_raiz = "electro/TANKS/"
buscar_subdirectorios(directorio_raiz)

# Combinar DataFrames en uno solo
if lista_dataframes:
    data_frame_final = pd.concat(lista_dataframes, ignore_index=True)
    print(f"Número de animales únicos: {data_frame_final['animal'].nunique()}")
    data_frame_final.to_csv('data_frame_final_ODD_ach.csv', index=False)
else:
    print("No se encontraron datos para procesar.")

# Mostrar errores encontrados
if errors:
    print("\nErrores encontrados:")
    for error in errors:
        print(error)

sys.exit()