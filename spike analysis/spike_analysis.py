# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tdt import read_block
from scipy.stats import pearsonr

# --- CONFIGURATION ---
# Base directory: folder where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# TANKS folder is one level above the script folder
tanks_folder = os.path.join(base_dir, '..', 'TANKS')

# Output folder for waveform figures
out_dir = os.path.join(base_dir, 'spike_waveforms')
os.makedirs(out_dir, exist_ok=True)

# --- LOAD BLOCK LIST FROM EXCEL ---
# Excel file must have headers in the first row.
# All columns are text except 'freqpair', which contains integers.
BlockList = pd.read_excel('BlockList.xlsx', dtype=str)
BlockList['freqpair'] = pd.to_numeric(BlockList['freqpair'], errors='coerce').astype('Int64')

# --- MAIN PROCESSING LOOP ---
results = []

block_id = [
    'control_block_1', 'control_block_2',
    'effect_block_1', 'effect_block_2',
    'rec_block_1', 'rec_block_2'
]

for _, row in BlockList.iterrows():
    tank = row['tank']
    unit = row['unit']
    freqpair = row['freqpair']

    spikes = []
    fs = None

    # Load spike data for each block
    for b in block_id:
        try:
            block_name = row[b]
            if isinstance(block_name, str) and block_name.strip():
                block_path = os.path.join(tanks_folder, tank, block_name)
                data = read_block(block_path)
                if hasattr(data, 'snips') and hasattr(data.snips, 'eNeu'):
                    spk = data.snips.eNeu.data  # amplitudes in volts
                    fs = data.snips.eNeu.fs
                    spikes.append(spk)
        except Exception as e:
            print(f"Failed {tank}, {unit}, {b}: {e}")

    if not spikes:
        continue

    spikes = np.vstack(spikes)
    nSpikes, nSamples = spikes.shape
    t = np.arange(nSamples) / fs

    # Compute mean and standard deviation of spike waveforms
    wave_mean = np.mean(spikes, axis=0)
    wave_std = np.std(spikes, axis=0)

# Plot waveform mean ± std
    plt.figure(figsize=(6, 4))
    std_fill = plt.fill_between(
        t * 1e3,
        (wave_mean + wave_std) * 1e6,
        (wave_mean - wave_std) * 1e6,
        color='0.8',
        edgecolor='none'
    )
    mean_line, = plt.plot(t * 1e3, wave_mean * 1e6, 'k', linewidth=1.5)

    plt.text(0.02, 0.95, f'n = {nSpikes}', transform=plt.gca().transAxes,
             ha='left', va='top', fontsize=10)
    plt.legend([mean_line, std_fill], ['mean', 'std'],
               loc='upper right', frameon=False, fontsize=9)

    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude (µV)')
    plt.xlim([0, t[-1] * 1e3])
    plt.title(f'Animal {tank}, Unit {unit}', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, f'{tank}_{unit}_spikes.jpg'))
    plt.close()

    # Spike polarity
    polarity = 'pos' if np.mean(wave_mean[60:80]) > 0 else 'neg'

    # Signal-to-noise ratio
    snr = np.max(np.abs(wave_mean)) / np.std(spikes)

    # Peak-to-peak amplitude
    ptp = np.max(wave_mean) - np.min(wave_mean)

    # Temporal jitter
    idx_min = np.argmin(spikes, axis=1)
    t_peak = (idx_min / fs) * 1e3
    jitter = np.std(t_peak)

    # Morphological variability (mean correlation with template)
    corrs = [pearsonr(spk, wave_mean)[0] for spk in spikes]
    mean_corr = np.mean(corrs)

    # Append results for this unit
    results.append({
        'Tank': tank,
        'Unit': unit,
        'FreqPair': freqpair,
        'Polarity': polarity,
        'N_Spikes': nSpikes,
        'SNR': snr,
        'PeakToPeak_(V)': ptp,
        'Jitter_(ms)': jitter,
        'MeanCorrelation': mean_corr
    })

# --- SAVE RESULTS ---
Results = pd.DataFrame(results)
Results.to_csv('SpikeQualityTable.csv', index=False)


