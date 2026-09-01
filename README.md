# Workshop on "Introduction to child-centered longform audio processing"

Introduction

## How to get started

- cloning this repository
- system preparations (git-lfs, ffmpeg, uv, datalad)
- submodule init recursive
- environment installation (uv or pip or conda)
- data download: VanDam (standard-converted wavs plus csv-converted annotations)
- if possible, most steps in 01_run_installations.sh, according to os


## Long-form data processing

- VanDam data preparation (02_run_data_preparation.py and config.yml)
- VTC plus metrics: 03_run_vtc.sh
- Speech Maturity plus metrics: 04_run_speech_maturity_classifier.sh 
- Babbling Recognition plus metrics: 05_run_barbar.sh plus ...
- Visualize results: 06_visualize_results.py 




