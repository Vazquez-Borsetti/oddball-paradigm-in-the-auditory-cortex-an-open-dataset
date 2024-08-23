# oddball-paradigm-in-the-auditory-cortex-an-open-dataset
Overview

This repository contains open datasets of neural recordings from the auditory cortex of rats, obtained during experiments using the oddball paradigm. The data aims to explore how the brain processes predictable versus unexpected auditory stimuli.
Dataset Description
The dataset includes multi-unit recordings of neuronal activity during the presentation of standard and deviant tones. The data is categorized by stimulus type and cortical sub-region.
Files Included

    xxxx.csv: The main dataset containing early low processed data of neuronal spike times and related metadata.
    Metadataxxx: Details of the experimental setup and recording parameters.
    README.md: This document.

Columns in neural_data.csv

    spike_times: Timestamps of neuronal spikes.
    stimulus_type: Type of stimulus (standard, deviant, after_deviant).
    DIVISION: Sub-region within the auditory cortex.
    ID: Unique identifier for each recording session.
    Cluster: Clustering information derived from spike train analysis.
    cat: Category of the stimulus condition.

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
