
import pandas as pd
import numpy as np # fundamental package for scientific computing, handles arrays and math
import matplotlib.pyplot as plt # standard Python plotting library
from matplotlib.ticker import MaxNLocator # so we can force integer tick labels later
import copy
import tdt
from tdt import read_block, epoc_filter
def data_estractor(BLOCK_PATH):
    
    REF_EPOC = 'Cond'
    SNIP_STORE = 'eNeu'
    SORTID = 'TankSort'
    CHANNEL = 3
    SORTCODE = 0          # set to 0 to use all sorts
    TRANGE = [-0.0, 0.25]

    
    # import data block into Python structure
    data = tdt.read_block(BLOCK_PATH) #,  export= 'csv') #evtype=['epocs', 'snips', 'scalars'], sortname=SORTID, channel=CHANNEL, nodata=1)
    try:
        del(data.epocs['Swee'].notes)# si no se borra las notes vacias da un error
    except Exception as e:
        print("Swee'.notes deleted in BLOCK_PATH")
    raster_data = tdt.epoc_filter(data, REF_EPOC,t=TRANGE)

    #print (data.epocs.Cond)#Freq.data
    hist_data = tdt.epoc_filter(data, REF_EPOC,t=TRANGE, tref=True)
    print('00000000000')
    #print(raster_data.snips[SNIP_STORE])
    if data.snips:
        ts = raster_data.snips[SNIP_STORE].ts
        #print(data.epocs)
        print(type(data.snips)) 
    else:
        #Crear las listas para las columnas del DataFrame
        all_x = []  # Para almacenar las spikes
        all_y = []  # Para almacenar los trials
        all_frec = []  # Para almacenar la frecuencia
        cond = []  # Para almacenar la condición
        arr=data.epocs.Cond.data
        print(arr)
        print('.................')
        # filtered_arr = arr[arr != -1]
        ntrial=0
        
        for i,trial in enumerate(arr):
        # Iterar sobre los trials
        # Omitir si el valor de la condición es -1
            if trial != -1:
                all_x.append(np.nan)  # Si las spikes no están disponibles, asignamos NaN
                all_y.append(ntrial)  # El número de trial
                all_frec.append(data.epocs.Freq.data[i])  # La frecuencia del trial
                cond.append(trial)  # El número de condición (1 o 2)
                ntrial=1+ntrial

        dfc = pd.DataFrame({
        'spikes': pd.Series(all_x, dtype=float),
        'trial': pd.Series(all_y, dtype=int),
        'frec': pd.Series(all_frec, dtype=float),
        'condition': pd.Series(cond, dtype=int),  # Especificar el tipo de dato 'int'
        'value': 1
        })
        print (dfc)
        return dfc

    num_trials = raster_data.time_ranges.shape[1]
    #print (ts)
    ig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(5, 8))

    hist_ts = hist_data.snips[SNIP_STORE].ts
    nbins = np.int64(np.floor(len(hist_ts)/10.))

    
    
    def condition(cond):
        all_ts = [[] for x in range(num_trials)]
        all_y = [[] for x in range(num_trials)]
        all_frec = np.array([])#[[] for x in range(num_trials)]
        for trial in range(num_trials):
            if data.epocs.Cond.data[trial]== cond:


                trial_on = raster_data.time_ranges[0, trial]
                trial_off = raster_data.time_ranges[1, trial]
                ind1 = ts >= trial_on
                ind2 = ts < trial_off
                trial_ts = ts[ind1 & ind2]
                all_ts[trial] = trial_ts - trial_on + TRANGE[0]
                all_y[trial] = trial * np.ones(len(trial_ts))
                all_frec = np.append(all_frec,data.epocs.Freq.data[trial])
                #print(data.epocs.Freq.data[trial])
                if len(trial_ts) == 0:
                    all_ts[trial] = np.array([np.nan])
                    all_y[trial] = np.array([trial])
                    all_frec = np.append(all_frec,data.epocs.Freq.data[trial])
        all_x = np.concatenate(all_ts)
        all_y = np.concatenate(all_y)
        dfc = pd.DataFrame()
        dfc['spikes']=pd.Series(all_x)
        dfc['trial']=pd.Series(all_y)
        dfc['frec']=pd.Series(all_frec)

        dfc['condition']=cond
        print(dfc.head(20))
        print(dfc.shape)
        return dfc

    dfs,dfd = condition(1),condition(2)  


    print(dfs['trial'].unique().shape)
    dft = pd.concat([dfs,dfd])
    print(dft.sample(10))


    
    return dft
    
# # #print(data.streams)
# data_frame_TEST=data_estractor('electro/TANKS/21_021/7-3-ODD-5-6-F1')
# # # # # path
# #data_frame_TEST=data_estractor('electro/TANKS/18_048/1-3-ASC-1-2-C1')

# print(data_frame_TEST.head())
# # # data_frame_final.to_csv('19_035_1-1-ASC-8-9-C1_ASC.csv',index=False)