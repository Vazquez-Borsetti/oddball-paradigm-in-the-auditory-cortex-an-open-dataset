README.TXT
-----------

Purpose
-------
spike_analysis.py processes spike waveform data extracted from TDT (Tucker-Davis Technologies) recording blocks.
It computes waveform statistics and quality metrics for each unit and generates plots and a summary table.

Folder Structure
----------------
The expected folder organization is:

[Parent folder]
│
├── TANKS\
│   ├── TANK1\
│   │   ├── BLOCK1\
│   │   ├── BLOCK2\
│   │   ├── BLOCK3\
│   │   ├── BLOCK4\
│   │   └── (other blocks...)
│   └── (other tanks...)
│
└── spikeanalysis\
    ├── BlockList.xlsx
    ├── spike_analysis.py
    └── (generated outputs)

- The script (spike_analysis.py) must be placed in the "spikeanalysis" folder.
- The TDT “tanks” folders must be located inside the "TANKS" folder, which is one directory level above the script.

Required Input File
-------------------
BlockList.xlsx

This Excel file defines which TDT blocks belong to each animal and unit.
It must be located in the same folder as the script (spikeanalysis).
The first row must contain column names.

Required columns:
tank                  - Name of the animal or tank folder inside TANKS
unit                  - Unit identifier
freqpair              - Numeric identifier for the frequency pair (integer)
control_block_1       - Name of control block 1 (folder name inside tank)
control_block_2       - Name of control block 2
effect_block_1        - Name of effect block 1
effect_block_2        - Name of effect block 2
rec_block_1           - Name of recovery block 1
rec_block_2           - Name of recovery block 2

Example row:
tank	unit	freqpair	control_block_1	control_block_2	effect_block_1	effect_block_2	rec_block_1	rec_block_2
18_048	2-1	1	ACH	2-1-ASC-1-2-C1	2-1-DESC-2-1-C1	2-1-ASC-1-2-F1	2-1-DESC-2-1-F1	2-1-ASC-1-2-F3	2-1-DESC-2-1-F3

Output Files
------------
1. Folder: spike_waveforms
   Created automatically in the same directory as the script.
   Contains one image per unit:
   <tank>_<unit>_spikes.jpg

   Each figure shows:
   - Mean spike waveform (black line)
   - ±1 standard deviation (gray area)
   - Spike count (top-left corner)

2. File: SpikeQualityTable.csv
   Summary table with one row per unit containing computed metrics.

   Column descriptions:
   Tank                   - Tank (animal) name
   Unit                   - Unit identifier
   FreqPair               - Frequency pair ID
   Polarity               - Waveform polarity: pos or neg
   N_Spikes               - Number of detected spikes
   SNR                    - Signal-to-noise ratio
   PeakToPeak_(V)         - Peak-to-peak amplitude (in volts)
   Jitter_(ms)            - Temporal jitter (standard deviation of spike times, in ms)
   MeanCorrelation        - Mean correlation coefficient between each spike and the average waveform

Notes
-----
- The script assumes that TDT block folders contain valid data readable by read_block() from the TDT Python SDK.
- Missing or inaccessible blocks will be reported in the console output but do not stop execution.
- The relative path configuration expects this directory structure; if folders are renamed or relocated, update tanks_folder accordingly in the script.
