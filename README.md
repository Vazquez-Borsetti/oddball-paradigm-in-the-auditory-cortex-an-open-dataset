# oddball-paradigm-in-the-auditory-cortex-an-open-dataset
Overview

This repository contains open datasets of neural recordings from the auditory cortex of rats, obtained during experiments using the oddball paradigm. The data aims to explore how the brain processes predictable versus unexpected auditory stimuli.
Dataset Description
The dataset includes multi-unit recordings of neuronal activity during the presentation of standard and deviant tones. The data is categorized by stimulus type and cortical sub-region.

Current Status

This dataset is in the early stage of development. Future updates will include more detailed analysis and additional data.

Files Included

    xxxx.csv: The main dataset containing early low processed data of neuronal spike times and related metadata.
    Metadataxxx: Details of the experimental setup and recording parameters.
    README.md: This document.

Columns in neural_data.csv:

spike: The time (in seconds) relative to the onset of the acoustic stimulus during a trial when a neuronal spike was recorded. If no spikes were recorded in a trial, this column contains NaN as a placeholder.

trial: The number identifying each trial within the experiment. A trial represents a single presentation of an acoustic stimulus.

frec: The frequency (in kHz) of the auditory stimulus presented during the trial.

condition: Encoded marker indicating the type of stimulus: 1 for standard tones and 2 for deviant tones.

animal: A code representing the subject (rat) in the experiment, composed of an animal number and the year.

tract: An identifier for the electrode tract; multiple neurons may have been recorded from a single tract.

neuron: The identifier for the specific neuron recorded during the experiment.

unit: The unit of analysis, referring to the individual neuron or neural cluster recorded.

oddball: Describes the two-tone sequence where one tone serves as the standard and the other as the deviant, with roles reversed in a secondary sequence.

DIVISION: Indicates the sub-structure within the auditory cortex where the neuron was recorded.

DEPTH (Z): The depth (in micrometers) of the electrode in the brain relative to the cortical surface, providing a measure of vertical positioning.

X (Rostro-Caudal): The rostro-caudal position (in micrometers) of the recording site within the cortex.

Y: The medio-lateral position (in micrometers) of the recording site within the cortex.

BF (kHz): The best frequency, defined as the frequency at which the neuron exhibits the highest response, measured in kHz.

TF (dBs): The threshold frequency, representing the lowest sound intensity level (in dBs) that elicits a response from the neuron.


Metadata

    Species: Rat
    Recording Region: Auditory cortex
    Stimuli: Standard tones (90%) and deviant tones (10%)
    Recording Techniques: [Details on recording methodology]
    Sampling Rate: [Sampling rate of recordings]

Data Processing and Analysis

    Python: Used for data processing and basic analysis.
    R: Used for generalized mixed models.

Citation

If you use this dataset in your research, please cite:

    [Your Citation Here]

License

This dataset is released under the [Your License Here] license.
Contact

For questions or more information, please contact [Your Contact Information].
