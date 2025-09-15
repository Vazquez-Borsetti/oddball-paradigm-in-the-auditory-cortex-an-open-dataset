# Neural Responses to Auditory Oddball Paradigm in Rat Auditory Cortex

## Overview
Open dataset of multi-unit recordings from the rat auditory cortex during oddball paradigm experiments and acetylcholine administration. The dataset explores neural coding of predictable versus unexpected auditory stimuli.

[Interactive visualization of the effects of acetylcholine on neuronal activity.](https://vazquez-borsetti.github.io/oddball-paradigm-in-the-auditory-cortex-an-open-dataset/)

**Core Metadata**  
- **DOI**: To be assigned upon publication  
- **License**: CC0 1.0
- **Keywords**: Auditory cortex, Extracellular electrophysiology, Deviance detection, Acetylcholine, Stimulus-specific adaptation  

## Dataset Files
| File Name               | Description                          | Key Columns                              |
|-------------------------|--------------------------------------|------------------------------------------|
| `oddball_dataset.csv`   | Primary neural recordings dataset    | `spikes`, `trial`, `freq`, `condition`, `division` |
| `odd_data_with_AD.csv`  | Includes after-deviant responses     | `cat`            |
| `df_aver_with_S_D_AD.csv` | Processed data with spike counts     | `S_counts`, `FR(s)`, `FR_norm` |

## Experimental Design
### Subjects
- **Species**: *Rattus norvegicus* (Sprague-Dawley)  
- **Sample**: 37 rats  
- **Ethics**: Approved per University of Salamanca Animal Care Committee and EU Directive 2010/63/EU  

### Stimulus Parameters
| Parameter       | Value          |
|-----------------|----------------|
| Paradigm        | Oddball (90% standard / 10% deviant) |
| Tone Duration   | 75 ms          |
| Intensity       | Variable (see `MT (dB)`) |
| Oddball Types   | Defined in `oddball` column |

### Recording Setup
- **Region**: Auditory cortex sub-regions (`DIVISION` column)  
- **Electrode**: Tungsten (1–3 MΩ)  
- **Coordinates**: Stereotaxic positions in µm (`depth (Z)`, `rostrocaudal (X)`, `mediolateral (Y)`)  

## Key Variables (oddball_dataset.csv)
| Column                | Description                          | Units/Format       |
|-----------------------|--------------------------------------|--------------------|
| `spikes`              | Spike time relative to stimulus      | Seconds (NaN = no spike) |
| `trial`               | Trial identifier                     | Integer            |
| `freq`                | Tone frequency                       | kHz                |
| `condition`           | Stimulus type                        | 1=Standard, 2=Deviant |
| `division`            | Cortical sub-region                  | Text (e.g., A1, AAF) |
| `BF (kHz)`            | Best frequency                       | kHz                |
| `MT (dB)`             | Minimum response threshold           | dB SPL             |
| `block_type`          | Experimental condition               | Text               |
| `animal_unit`         | Unique neuron identifier             | Composite ID       |

## Advanced Variables (Other Files)
- **Response Metrics**: `FR(s)` (Firing rate), `FR_norm` (Normalized firing)  
- **Condition Categories**: `cat` (Standard/Deviant/After-Deviant), 
- **Spike Analysis**: `S_counts` (Spike counts), `ms` (Time bins/milliseconds)  

## Usage
```python
import pandas as pd

# Load primary dataset
df = pd.read_csv("oddball_dataset.csv")

# Example: Filter A1 neurons
a1_neurons = df[df['division'] == 'A1']
