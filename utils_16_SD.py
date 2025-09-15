# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(PV)s
"""


import pandas as pd
import numpy as np  # fundamental package for scientific computing, handles arrays and math
import matplotlib
import matplotlib.pyplot as plt  # standardd Python plotting library
from matplotlib.ticker import MaxNLocator  # so we can force integer tick labels later
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from scipy.stats import gaussian_kde
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None
pd.options.display.max_rows = None
fign=0






def average_oddball(df):
    df_average = pd.DataFrame()

    # Iterar por cada animal_unit
    for animal_unit_group, datos_grupo in df.groupby('animal_unit'):
        df_average_odd = pd.DataFrame()

        # Aplicar rangos a cada grupo oddball-block_type
        for (oddball_val, block_type), datos_oddball in datos_grupo.groupby(['oddball', 'block_type']):
            un_oddb = rangos(datos_oddball)
            df_average_odd = pd.concat([df_average_odd, un_oddb], ignore_index=True)

        # Calcular medias de standard en control_block_1 y control_block_2
        ctrl1 = df_average_odd.query("block_type == 'control_block_1' and cat == 'standard'")
        ctrl2 = df_average_odd.query("block_type == 'control_block_2' and cat == 'standard'")
        media_standard_1 = ctrl1['FR(s)'].mean() if not ctrl1.empty else None
        media_standard_2 = ctrl2['FR(s)'].mean() if not ctrl2.empty else None
        print(media_standard_1)
        # Asignar media y normalizar según block_type
        def asignar_norma(row):
            if row['block_type'] in ['control_block_1', 'effect_block_1', 'rec_block_1']:
                media = media_standard_1
            elif row['block_type'] in ['control_block_2', 'effect_block_2', 'rec_block_2']:
                media = media_standard_2
            else:
                media = None

            row['mean_standard_FR(s)'] = media
            row['FR_norm'] = row['FR(s)'] / media if media and media != 0 else None
            return row

        df_average_odd = df_average_odd.apply(asignar_norma, axis=1)

        # Acumular resultados
        df_average = pd.concat([df_average, df_average_odd], ignore_index=True)

    return df_average


def rangos(df_raw_odd):
    #print(df_raw_odd.shape)
    # Conservar una copia de las columnas originales
    original_columns = df_raw_odd.columns.tolist()
    
    trials = df_raw_odd.groupby('cat')['trial'].nunique().rename('trials')
    df_raw_odd.reset_index(drop=True, inplace=True)
    
    labels = [0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]
    spikes_nonan = df_raw_odd['spikes'].dropna()
    
    # Manejar caso donde todos los spikes son NaN
    if spikes_nonan.empty:
        # Crear DataFrame vacío con estructura requerida
        unique_cats = df_raw_odd['cat'].unique()
        df_raw_odd_piv = pd.DataFrame(0, index=unique_cats, columns=labels)
        df_raw_odd_piv.index.name = 'cat'
        df_raw_odd_piv = df_raw_odd_piv.stack().reset_index()
        df_raw_odd_piv.rename(columns={0: 'S_counts'}, inplace=True)
    else:
        # Asignar rangos temporales
        df_raw_odd['ms'] = pd.cut(df_raw_odd['spikes'], bins=10, labels=labels)
        
        # Crear tabla pivote asegurando todas las categorías y bins
        df_raw_odd_piv = df_raw_odd.pivot_table(
            index='cat',
            columns='ms',
            aggfunc='size',
            fill_value=0,
            observed=True
        )
        
        # Reindexar para incluir todas las categorías y bins
        unique_cats = df_raw_odd['cat'].unique()
        df_raw_odd_piv = df_raw_odd_piv.reindex(
            index=unique_cats,
            columns=labels,
            fill_value=0
        )
        
        # Stackear y formatear
        df_raw_odd_piv = df_raw_odd_piv.stack().reset_index()
        df_raw_odd_piv.rename(columns={0: 'S_counts'}, inplace=True)

    # Combinar con trials
    df_raw_odd_piv = pd.merge(
        df_raw_odd_piv,
        trials.reset_index(),
        on='cat',
        how='left'
    )
    
    # Eliminar columnas temporales y conservar metadata
    cols_to_drop = ['spikes', 'trial', 'ms', 'cat']
    metadata_columns = [col for col in original_columns if col not in cols_to_drop]
    metadata = df_raw_odd[metadata_columns].iloc[0].to_dict()
    
    # Añadir metadata al DataFrame final
    for col, val in metadata.items():
        df_raw_odd_piv[col] = val
    
    # Calcular métricas finales
    df_raw_odd_piv['FR(s)'] = df_raw_odd_piv['S_counts'] * 40 / df_raw_odd_piv['trials']
    #df_raw_odd_piv['mean_FR(s)'] = df_raw_odd_piv['FR(s)'].mean()
    
    sums = df_raw_odd_piv.groupby('cat')['FR(s)'].sum().reset_index()
    sums = sums.rename(columns={'FR(s)': 'FR_agg'})
    
    df_raw_odd_piv = df_raw_odd_piv.merge(sums, on='cat', how='left')
    #df_raw_odd_piv['FR_norm'] = df_raw_odd_piv['FR(s)'] / df_raw_odd_piv['mean_FR(s)']
    
    return df_raw_odd_piv

def pdf_rasters(df):
    matplotlib.use('Agg', force=True)
    unidades_animales_unicas = df['animal_unit'].unique()
    # Crear un archivo PDF para guardar las figuras
    pdf_filename = "auditory_cortex_neurons.pdf"
    # Crear un archivo PDF para guardar las figuras
    pdf_pages= PdfPages(pdf_filename) 
    
    # Iterar sobre cada unidad animal y guardar las figuras en el PDF
    for animal_unit in unidades_animales_unicas:
        # Filtrar el DataFrame para obtener datos específicos de la unidad animal actual
        df_animal_unit = df[df['animal_unit'] == animal_unit]
        
        fig = figure_1_rasters_SD(df_animal_unit)
        
        
        # Añadir un título a la figura
        fig.suptitle('Unidad/Animal: {0},DIVISION: {1}'.format(animal_unit,df_animal_unit['division'].unique()))
        
        pdf_pages.savefig(fig)
        
        # Cerrar la figura para liberar memoria
        plt.close(fig)


    # Cerrar el archivo PDF después de guardar todas las figuras
    pdf_pages.close()

    print("Se han guardado todas las figuras en", pdf_filename)


def SD_panel_1_combined(df, neuron_list):
    # Configuración de figura principal (figure 3)
    fig = plt.figure(figsize=(10, 8 + 3*len(neuron_list)))  # Más espacio vertical
    gs_main = gridspec.GridSpec(1, len(neuron_list), figure=fig, wspace=0.3)  # Separación entre columnas de neuronas
    
    for idx, neuron in enumerate(neuron_list):
        neuron_data = df[df['animal_unit'] == neuron]
        
        # Subgrid con más espacio interno
        gs_sub = gridspec.GridSpecFromSubplotSpec(6, 2, subplot_spec=gs_main[idx], 
                                                hspace=0.4,  # Más espacio vertical entre filas de subpaneles
                                                wspace=0.3)  # Más espacio horizontal entre columnas
        
        # Paneles
        plot_raster_subpanel(neuron_data, 'control_block_1', 'control_block_2', gs_sub, [0, 1], 'CTL')
        plot_raster_subpanel(neuron_data, 'effect_block_1', 'effect_block_2', gs_sub, [2, 3], 'ACH')
        plot_raster_subpanel(neuron_data, 'rec_block_1', 'rec_block_2', gs_sub, [4, 5], 'REC', xlabel=True)

    # Ajustes finales
    fig.tight_layout(pad=1)
    plt.savefig("Figure_3.tif", dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.savefig("Figure_3.pdf", bbox_inches='tight', pad_inches=0.05)
    plt.show()

def plot_raster_subpanel(df, block1, block2, gs_sub, rows, label, xlabel=False):
    df_block1 = df[df['block_type'] == block1]
    df_block2 = df[df['block_type'] == block2]

    # Crear subplots
    ax1 = plt.subplot(gs_sub[rows[0], 0])
    ax2 = plt.subplot(gs_sub[rows[1], 0])
    ax3 = plt.subplot(gs_sub[rows[0], 1])
    ax4 = plt.subplot(gs_sub[rows[1], 1])

    # Graficar
    plot_raster(df_block1, ax1, ax2)
    plot_raster(df_block2, ax3, ax4)

    # Ajustar decimales del eje Y
    for ax in [ax1, ax2, ax3, ax4]:
         # <-- 1 decimal
        ax.tick_params(axis='both', labelsize=8)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(0.05))
        ax.set_xlim(-0.02, 0.25)
        if ax==ax2 or ax==ax4:
            ax.set_ylim(-0.02, 400)
        else:
            ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f')) 
            
        ax.margins(x=0.02, y=0.05)

    # Etiquetas
    ax1.set_ylabel('Count/trial', fontsize=9, labelpad=2)  # Reducir padding
    if xlabel:
        ax2.set_xlabel('Trial Window, s', fontsize=9, labelpad=2)
        ax4.set_xlabel('Trial Window, s', fontsize=9, labelpad=2)
    
    # Texto de la etiqueta
    ax1.text(0.95, 0.88, label, transform=ax1.transAxes, 
            fontsize=10, va='top', ha='right', 
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1.5))
    
def figure_1_rasters_SD(df):
    # Create a large figure
    fig = plt.figure(figsize=(15, 20))
    # Create a GridSpec with 6 rows and 2 columns
    gs = gridspec.GridSpec(6, 2, figure=fig)
    
    # Panel 1
    df_control_1 = df[df['block_type'] == 'control_block_1']
    df_control_2 = df[df['block_type'] == 'control_block_2']
    ax1_1 = fig.add_subplot(gs[0, 0])
    ax1_1.set_ylabel('Count/trial', fontsize=11)
    ax1_2 = fig.add_subplot(gs[1, 0])
    ax1_3 = fig.add_subplot(gs[0, 1])
    ax1_4 = fig.add_subplot(gs[1, 1])
    plot_raster(df_control_1, ax1_1, ax1_2)
    plot_raster(df_control_2, ax1_3, ax1_4)
    ax1_1.text(0.9, 0.95, 'CTL', transform=ax1_1.transAxes, fontsize=14, va='top', ha='right')

    # Panel 2
    df_effect_1 = df[df['block_type'] == 'effect_block_1']
    df_effect_2 = df[df['block_type'] == 'effect_block_2']
    ax2_1 = fig.add_subplot(gs[2, 0])
    ax2_1.set_ylabel('Count/trial', fontsize=11)
    ax2_2 = fig.add_subplot(gs[3, 0])
    ax2_3 = fig.add_subplot(gs[2, 1])
    ax2_4 = fig.add_subplot(gs[3, 1])
    plot_raster(df_effect_1, ax2_1, ax2_2)
    plot_raster(df_effect_2, ax2_3, ax2_4)
    ax2_1.text(0.9, 0.95, 'ACH', transform=ax2_1.transAxes, fontsize=14, va='top', ha='right')

    # Panel 3
    df_rec_1 = df[df['block_type'] == 'rec_block_1']
    df_rec_2 = df[df['block_type'] == 'rec_block_2']
    ax3_1 = fig.add_subplot(gs[4, 0])
    ax3_1.set_ylabel('Count/trial', fontsize=11)
    ax3_2 = fig.add_subplot(gs[5, 0])
    ax3_2.set_xlabel('Trial Window, s', fontsize=11)
    ax3_3 = fig.add_subplot(gs[4, 1])
    ax3_4 = fig.add_subplot(gs[5, 1])
    ax3_4.set_xlabel('Trial Window, s', fontsize=11)
    plot_raster(df_rec_1, ax3_1, ax3_2)
    plot_raster(df_rec_2, ax3_3, ax3_4)
    ax3_1.text(0.9, 0.95, 'REC', transform=ax3_1.transAxes, fontsize=14, va='top', ha='right')
    
    
    # Apply margins and scaling to all axes
    for ax in fig.axes:
        ax.set_xlim(-0.01, 0.26)  # Fijar el rango global para todos los ejes
        ax.margins(x=0, y=0.1)  # Márgenes adicionales en y, pero no en x

    # Display and return the figure
    plt.show()
    return fig

def plot_raster(oddball_df,ax1, ax2):
    
    """
    Plots raster and histogram for spike data categorized as 'standard', 'deviant', and 'after_deviant'.
    
    Parameters:
    oddball_df (DataFrame): DataFrame containing spike data with categorical labels.
    """
    
        
    # Filter data based on the category
    standard_spikes = oddball_df[oddball_df['cat'] == 'standard']
    deviant_spikes = oddball_df[oddball_df['cat'] == 'deviant']
    after_deviant_spikes = oddball_df[oddball_df['cat'] == 'after_deviant']
    
    # Get the number of unique trials for standard and deviant categories
    num_standard_trials = standard_spikes['trial'].nunique()
    num_deviant_trials = deviant_spikes['trial'].nunique()
    num_a_deviant_trials = after_deviant_spikes['trial'].nunique()
    

    # Get spike times for each category
    standard_spike_times = standard_spikes['spikes']
    deviant_spike_times = deviant_spikes['spikes']
    after_deviant_spike_times = after_deviant_spikes['spikes']
    
    # Define the number of bins for the histogram
    num_bins = 10  # Adjust the number of bins as needed
    #print(num_bins)
    common_range=(0,0.25)
    # Calculate weights for the histograms to normalize the counts
    standard_weights = np.ones_like(standard_spike_times) / len(standard_spike_times)
    deviant_weights = np.ones_like(deviant_spike_times) / len(deviant_spike_times)
    after_deviant_weights = np.ones_like(after_deviant_spike_times) / len(after_deviant_spike_times)
    # weights=[standard_weights,deviant_weights,after_deviant_weights]
    # sns.histplot(data=oddball_df, x='spikes', hue='cat', bins=10,weights=weights, multiple='dodge', shrink=0.8)
    
    # Plot histograms
    ax1.hist(standard_spike_times, bins=num_bins, color='blue',range=common_range, weights=standard_weights, histtype='step', lw=1.5)
    ax1.hist(deviant_spike_times, bins=num_bins, color='red',range=common_range, weights=deviant_weights, histtype='step', lw=1.5)
    ax1.hist(after_deviant_spike_times, bins=num_bins, color='green',range=common_range, weights=after_deviant_weights, histtype='step', lw=1.5)
    
    ax1.hist(standard_spike_times, bins=num_bins, color='blue',range=common_range, weights=standard_weights, alpha=0.2, label='standard')
    ax1.hist(deviant_spike_times, bins=num_bins, color='red',range=common_range, weights=deviant_weights, alpha=0.2, label='Deviant')
    ax1.hist(after_deviant_spike_times, bins=num_bins, color='green',range=common_range, weights=after_deviant_weights, alpha=0.2, label='After Deviant')
    # Customize the histogram plot
    ax1.axis('tight')
    ax1.axvline(x=0.0, color='black', linestyle='-', alpha=0.5)
    ax1.axvline(x=0.075, color='black', linestyle='--', alpha=0.5)
    
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    # Get trial numbers and spike times for raster plot
    standard_trial_numbers = standard_spikes['trial']
    deviant_trial_numbers = deviant_spikes['trial']
    after_deviant_trial_numbers = after_deviant_spikes['trial']
    # Plot raster plot
    ax2.plot(standard_spike_times, standard_trial_numbers, 'b.', markersize=3)
    ax2.plot(deviant_spike_times, deviant_trial_numbers, 'r.', markersize=3)
    ax2.plot(after_deviant_spike_times, after_deviant_trial_numbers, 'g.', markersize=3)
    # Customize the raster plot
    ax2.axis('tight')
    
    ax2.axvline(x=0.0, color='black', linestyle='-', alpha=0.5)
    ax2.axvline(x=0.075, color='black', linestyle='--', alpha=0.5)
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

    
    plt.show()
    return ax1, ax2


def after_deviant(df):
    groups =df.groupby(['oddball'])#,'condition'
    df_with_S_D_AD= pd.DataFrame()
    #df_with_D_AD_before_s= pd.DataFrame()
    for oddball,group in groups:
        # Check if there are any NaN values in the 'trial' column of the current group
        #print(group['trial'].nunique())
        if group['trial'].isna().any():
            print(group)
            group = group.copy()
            group['trial'] = group['trial'].fillna(0)

            # Crear nuevas filas manualmente
            new_rows = pd.DataFrame([
                {'oddball': oddball, 'trial': 0, 'cat': 'standard'},
                {'oddball': oddball, 'trial': 0, 'cat': 'deviant'},
                {'oddball': oddball, 'trial': 0, 'cat': 'after_deviant'}
            ])

            # Concatenar los datos originales con las nuevas filas
            group = pd.concat([group, new_rows], ignore_index=True)

            df_with_S_D_AD = pd.concat([df_with_S_D_AD, group], ignore_index=True)
            break
        condition2=group.groupby('condition')#,
        
        group_D = condition2.get_group(2).copy()
        
        group_D.loc[:, 'cat'] = 'deviant'
        group_D.loc[:, 'cat2'] = 'deviant'
        group_D['trial'] = group_D['trial'].astype(int)
        
        group_S = condition2.get_group(1).copy()
        group_S['trial'] = group_S['trial'].astype(int)
        
        # Encuentra los trials después de los trials deviant
        A_deviant_trials = (group_D['trial'].unique() + 1).tolist()
        
        group_AD = group_S.loc[group_S['trial'].isin(A_deviant_trials)].copy()#lambda x: x['year'].isin(years)
                
        group_AD.loc[:, 'cat'] = 'after_deviant'
        group_AD.loc[:, 'cat2'] = 'after_deviant'
        before_deviant_trials = (group_D['trial'].unique() - 1).tolist()
        
        
        group_S=group_S[~group_S['trial'].isin(group_D['trial'].unique()+1)]#group_S[~group_AD[group_S].isin(valores_a_excluir)]
        group_S['cat'] = 'standard'
        group_S['cat2'] = None
        group_S.loc[group_S['trial'].isin(before_deviant_trials), 'cat2'] = 'standard'

        
        counts_by_trial = pd.concat( [group_S,group_D,group_AD], ignore_index=True)
        
        df_with_S_D_AD=pd.concat([df_with_S_D_AD,counts_by_trial])
        
    return df_with_S_D_AD

def calculate_correlation_matrix(subset_df):
    #print(subset_df.head())
    # Crear pivot table
    pivot_df = subset_df.pivot_table(index='merged_column', columns='ms', values='FR_norm')
    #print(pivot_df)
    # Filtrar filas que NO son todos ceros
    pivot_df = pivot_df.loc[~(pivot_df == 0).all(axis=1)]
    #print('***********************')
    # Unir con los datos originales
    merged_df = pivot_df.merge(subset_df, on='merged_column', how='left')
    
    merged_df = merged_df.select_dtypes(include=["number"])
    #print(merged_df)
    # Eliminar columnas no necesarias
    merged_df = merged_df.drop(columns=["FR_agg", "ms", "S_counts", "trials", 
                                         "condition", "tract", "FR_norm", "FR(s)", "mean_FR(s)",
                                       'mean_standard_FR(s)',             'level_1'], errors='ignore')
    #print ('GGGGGGGGGGGGG')
    #print(f"Datos procesados:\n", merged_df.head())
    #print(merged_df.columns)
    
    # Calcular matriz de correlación
    correlation_matrix = merged_df.corr()
    return correlation_matrix

def correl_matrix(df):
    df.rename(columns={'rostrocaudal (X)': 'RC (x)', 'mediolateral (Y)': 'ML (y)','depth (Z)': 'depth (z)'}, inplace=True)
    
    col_data = df.pop('depth (z)')  # Saca la columna
    df.insert(15, 'depth (z)', col_data)  # Insertala en la posición 0print (df.sample())
    # Filtrar datos balanceados
    df_balanced = df.dropna(subset=['cat2'])
    df_balanced = average_oddball(df_balanced)
    
    #print('***********************')
    #print(df_balanced.head())
    
    # Ajustar valores de la columna 'ms'
    df_balanced['ms'] = pd.to_numeric(df_balanced['ms']).round(3)
    df_balanced.loc[df_balanced['cat'] == 'after_deviant', 'ms'] += 0.25
    df_balanced.loc[df_balanced['cat'] == 'standard', 'ms'] -= 0.25
    
    #sys.exit()
    
    df_balanced['ms'] = df_balanced['ms'].round(3)
    
    # Crear subsets de control, efecto y recuperación
    df_control = df_balanced[df_balanced['block_type'].isin(['control_block_1', 'control_block_2'])]
    df_effect = df_balanced[df_balanced['block_type'].isin(['effect_block_1', 'effect_block_2'])]
    df_rec = df_balanced[df_balanced['block_type'].isin(['rec_block_1', 'rec_block_2'])]
    #print(df_control.head())
    

    # Calcular matrices de correlación
    correlation_control = calculate_correlation_matrix(df_control)
    correlation_effect = calculate_correlation_matrix(df_effect)
    correlation_rec = calculate_correlation_matrix(df_rec)
    # Crear máscara para ocultar triángulo superior
    mask = np.triu(np.ones_like(correlation_control, dtype=bool))
    import matplotlib.pyplot as plt
    import seaborn as sns
    import matplotlib.gridspec as gridspec
    
    # Crear figura con GridSpec y un eje extra para la barra
    fig = plt.figure(figsize=(18, 6))
    gs = gridspec.GridSpec(1, 4, width_ratios=[1, 1, 1, 0.05], figure=fig)
    axes = [fig.add_subplot(gs[0, i]) for i in range(3)]
    cax = fig.add_subplot(gs[0, 3])
    
    titles = ["Control", "ACH", "Recovery"]
    correlation_matrices = [correlation_control, correlation_effect, correlation_rec]
    
    # Calcular límites comunes de colores
    vmin = min(m.values.min() for m in correlation_matrices)
    vmax = max(m.values.max() for m in correlation_matrices)
    
    ims = []
    for i, (ax, matrix, title) in enumerate(zip(axes, correlation_matrices, titles)):
        im = sns.heatmap(
            matrix,
            mask=mask,
            cmap="coolwarm",
            center=0,
            vmin=vmin, vmax=vmax,
            linewidths=0.5,
            ax=ax,
            cbar=False,     # Sin barra individual
            annot=False,
            yticklabels=True,
            xticklabels=True
        )
        ims.append(im)
        ax.set_title(title, fontsize=12, weight="bold")
    
       # Líneas negras que se frenan en la diagonal (no pisan el triángulo enmascarado)
        n = matrix.shape[0]
        for y in [10, 20, 30]:
            if not (0 <= y <= n):
                continue
            # Horizontal: de x=0 hasta la diagonal (x=y)
            ax.plot([0, min(y, n)], [y, y], color="black", linewidth=1, zorder=3)
            # Vertical: desde la diagonal hacia abajo
            ax.plot([y, y], [y, n], color="black", linewidth=1, zorder=3)
    
        
        # Solo mostrar etiquetas verticales en el primer subplot
        if i != 0:
            ax.set_yticklabels([])
    
        ax.tick_params(labelsize=10)
    
    # Agregar barra de color única sin superponer nada
    fig.colorbar(ims[0].collections[0], cax=cax)
    
    # Ajustar espacios automáticamente
    plt.tight_layout()



   # # Crear figura para los heatmaps
   #  fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)
   #  titles = ["Control", "ACH", "Recovery"]
   #  correlation_matrices = [correlation_control, correlation_effect, correlation_rec]
    
   #  # Crear heatmaps
   #  for i, (ax, matrix, title) in enumerate(zip(axes, correlation_matrices, titles)):
   #      # Mostrar el heatmap
   #      sns.heatmap(
   #          matrix, 
   #          cmap='coolwarm', 
   #          center=0, 
   #          linewidths=0.5, 
   #          ax=ax, 
   #          cbar=True, 
   #          annot=False,
   #          yticklabels=True  # Forzar que se muestren los nombres de filas
   #      )
        
   #      ax.set_title(title, fontsize=12, weight='bold')
        
   #      # Líneas negras de separación
   #      for y in [10, 20, 30]:
   #          ax.axhline(y=y, color='black', linewidth=1)
   #          ax.axvline(x=y, color='black', linewidth=1)
        
   #      # Solo mostrar labels verticales en el primer subplot
   #      if i != 0:
   #          ax.set_yticklabels([])  # Oculta los nombres de filas en los subplots 2 y 3
    
   #      ax.tick_params(labelsize=10)
    
    # Mostrar figura
    #plt.suptitle("Correlation Matrices Across Block Types", fontsize=16, weight='bold')
    plt.savefig("correlation_matrices.pdf", format="pdf", bbox_inches="tight")
    plt.savefig("correlation_matrices.tif", dpi=300, bbox_inches="tight")
    plt.show()

def figure4(df):
    results = []
    # df=df.fillna(0)
    # rows_with_nan = df[df.isna().any(axis=1)]

    # print(rows_with_nan)
    # Iterar sobre cada unidad experimental
    for animal_unit, group_df in df.groupby('animal_unit'):
        #print (group_df.sample(10))
        # Calcular FR para cada combinación de bloque y categoría
        fr_data = {}
        
        # Definir todas las combinaciones posibles
        blocks = ['control_block_1', 'control_block_2', 'effect_block_1', 'effect_block_2']
        categories = ['standard', 'deviant', 'after_deviant']
        
        for block in blocks:
            for cat in categories:
                # Filtrar y calcular media
                mask = (group_df['block_type'] == block) & (group_df['cat'] == cat)
                group_df.fillna(0, inplace=True)
                fr_value = group_df.loc[mask, 'FR(s)'].mean()
                fr_data[f'{block}_{cat}'] = fr_value
        
        # Calcular diferencias normalizadas para cada categoría
        norm_difs = {}
        for cat in categories:
            try:
                control = fr_data[f'control_block_2_{cat}']
                effect = fr_data[f'effect_block_2_{cat}']
                #print (effect)
                denominator = (control + effect)
                norm_dif = (control - effect)/denominator if denominator != 0 else 0
                norm_difs[f'norm_dif_{cat}'] = norm_dif
            except KeyError:
                norm_difs[f'norm_dif_{cat}'] = None
        
        # Guardar resultados con estructura clara
        results.append({
            'animal_unit': animal_unit,
            **fr_data,
            **norm_difs
        })

    # Convertir resultados a DataFrame
    results_df = pd.DataFrame(results)
    

   

    # Transformar DataFrame a formato largo
    melted_df = pd.melt(
        results_df,
        id_vars=['animal_unit'],
        value_vars=[f'norm_dif_{cat}' for cat in categories],
        var_name='category',
        value_name='normalized_difference'
    )

    # Mapear nombres más legibles
    category_names = {
        'norm_dif_standard': 'Standard',
        'norm_dif_deviant': 'Deviant',
        'norm_dif_after_deviant': 'After Deviant'
    }
    melted_df['category'] = melted_df['category'].map(category_names)

    # Definir paleta personalizada
    custom_palette = {
        'Standard': '#1f77b4',  # Azul
        'Deviant': '#d62728',   # Rojo
        'After Deviant': '#2ca02c'  # Verde
    }
    
    # Crear histograma con separación entre grupos
    plt.figure(figsize=(12, 7))
    
      # Proporción de reducción de las barras
    
        # Crear bins y convertirlos a categoría
    # Crear bins
    bins = 10
    melted_df['bin'] = pd.cut(melted_df['normalized_difference'], bins=bins, include_lowest=True)
    # Crear etiquetas simplificadas (centro del bin, redondeado)
    melted_df['bin'] = melted_df['bin'].apply(
        lambda x: pd.Interval(left=round(x.left, 1), right=round(x.right, 1), closed=x.closed)
    )
    print(melted_df)
    melted_df['bin_str'] = melted_df['bin'].astype(str)
    
    # Contar elementos por bin y categoría
    counts = melted_df.groupby(['bin_str','category']).size().reset_index(name='count')
    counts['bin_str'] = pd.Categorical(counts['bin_str'], 
                                  categories=[str(b) for b in melted_df['bin'].cat.categories], 
                                  ordered=True)


    ax = sns.barplot(
        data=counts,
        x='bin_str',      # eje x categórico
        y='count',        # altura = número de elementos por bin
        hue='category',
        palette=custom_palette,
        saturation=.75
    )
   
    # Mejorar etiquetas y estética
    plt.xlabel('Normalized Difference', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.title('Histogram of Normalized Difference by Category', fontsize=14)
    plt.legend(title='Category', fontsize=10)
    sns.despine()
    
    # Personalización del gráfico
    #plt.axvline(0, color='gray', linestyle='--', alpha=0.8)
    plt.title('Distribution of Normalized Differences in Firing Rate by Stimulation Type', pad=20)
    plt.xlabel('Normalized Differences (Control - ACh)/(Control + ACh)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.grid(alpha=0.2)
    
    # Ajustar la leyenda correctamente
    handles, labels = ax.get_legend_handles_labels()
    legend_patches = [
        mpatches.Patch(color=custom_palette['Standard'], label='Standard'),
        mpatches.Patch(color=custom_palette['Deviant'], label='Deviant'),
        mpatches.Patch(color=custom_palette['After Deviant'], label='After Deviant')
    ]

    # Agregar la leyenda
    plt.legend(
        handles=legend_patches,
        title='Stimulation',
        title_fontsize=12,
        fontsize=10,
        loc='upper left',
        frameon=True,
        framealpha=0.9
    )
    # Añadir anotaciones
    plt.text(0.8, 0.95, f'N = {len(results_df)} unidades', 
             transform=plt.gca().transAxes, ha='right')
    plt.savefig("Figure_4.tif", dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.savefig("Figure_4.pdf", bbox_inches='tight', pad_inches=0.05)
    plt.show()
    return melted_df