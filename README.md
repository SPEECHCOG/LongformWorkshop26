# Workshop on "Introduction to child-centered longform audio processing"

This repository is a step-by-step tutorial to use long-form analysis tools in practice. If you run into trouble with any of the tools, you might lack some of the required installations. In that case, refer to technical setup files in this repository.

Note: If you lack sudo / admin rights on your computer, some of the installations might not work. 

Relevant sections for cloning this repo, installing the example data, or converting your own data:

- [repository cloning](#repository-installation)
- [example data download](#example-data-download)
- [data conversion](#data-conversion)

Overview on how to run the tools:

- [Voice Type Classifier (VTC)](#speaker-diarization)
- [Speech Maturity Classifier](#child-speech-analysis-i-speech-maturity-classification)
- [Babbling Recognizer (BaBAR)](#child-speech-analysis-ii-babbling-recognition)
- [Linguistic Unit Count Estimation (ALICE)](#caregiver-speech-analysis-word-count-estimation)

If you use longform data analaysis tools for your research, please recognize the authors in the [references section](#references). You might want to check out our collection of [interesting links](#further-information).


## How to get started

We recommend to store all tools in one directory called LONGFORM_TOOLS located in home directory. In case you use your own folder structure, please avoid directory names that contain space characters (replace f.ex. with underscores). Open a terminal, and create the folder with these commands:

```bash
cd ~					# navigate to home directory
mkdir LONGFORM_TOOLS    # create a new folder called "LONGFORM_TOOLS"
cd LONGFORM_TOOLS       # navigate to empty folder "LONGFORM_TOOLS"
ls                      # should yield an empty line
```

### Repository installation

In general, you can clone any public repository from Github by navigating to its homepage, clicking the green button "Code", copying the HTTPS-key and running "git clone HTTPS-link" (replace "HTTPS-link" with the actual link). Let's get started by cloning [this repository](https://github.com/SPEECHCOG/LongformWorkshop26):

```bash
cd ~/LONGFORM_TOOLS		# navigate to directory LONGFORM_TOOLS to place the repository there
git clone https://github.com/SPEECHCOG/LongformWorkshop26.git
```

### Example Data Download

As example data, we use one recording from the publically available [VanDam corpus](https://gin.g-node.org/LAAC-LSCP/vandam-data/src/master). Execute this code in your terminal from LONGFORM_TOOLS directory. Note that this requires FFmpeg since we chunk the downloaded audio file. For installations, refer to the technical_setup files.

```bash
cd LongformWorkshop26	# if you cannot find the directory, try: cd ~/LONGFORM_TOOLS/LongformWorkshop26
bash code/data_download.sh
```

Note: If you would like to use your own data, please place it into LongformWorkshop26/data/recordings and run [data conversion](#data-conversion) to make the further pipelines work! The data directory is ignored by git, so your data will not be tracked by or transfered to Github.

### Data conversion 

Note: If you are using the example data, you may skip this part! 

Most of the tools expect the recordings in .wav format with 16kHz sampling rate. To convert your own data into expected formats, we prepared different scripts depending on the input type for you. Make sure your data is located in data/recordings folder, then execute the following lines in your terminal from LongformWorkshop26 directory:

```bash
cd ~/LONGFORM_TOOLS/LongformWorkshop26/data/recordings
bash ../../code/mp4_converter.sh                		# for video to audio (.wav) conversion 
bash ../../code/mp3_converter.sh						# for .mp3 to .wav conversion
bash ../../code/wav_converter.sh						# for .wav resampling to 16kHz mono-channel
```

The scripts create a subdirectory "wav" where they place the converted files.

## Long-form data processing

Let's get started with the actual data processing! Every section follows the structure: 1. input: what does the tool receive? 2. output: what does the tool return? 3. parameters: what parameters can be set to modify the tool outputs? 4. code: how to run the tool.

### Speaker diarization

The [Voice Type Classifier](https://github.com/LAAC-LSCP/VTC/tree/main) (VTC) determines who speaks when in an given audio file: It performs segmentation of the recording, classifying the segments where at least one speaker is active into the broad categories of female (FEM), male (MAL), key-child (KCH), and other children's (OCH) speech. Create an output directory first, then install the repository:

```bash
cd ~/LONGFORM_TOOLS										# navigate to LONGFORM_TOOLS to place the repository there
mkdir -p LongformWorkshop26/data/results/VTC_outputs	# create directory for outputs
git lfs install											
git clone --recurse-submodules https://github.com/LAAC-LSCP/VTC.git
cd VTC													# navigate to VTC folder
sh check_sys_dependencies.sh							# verify system requirements
uv sync													
```

If one of the above commands fails, refer to technical_setup_mac_linux file and follow the installation steps required for VTC.

1. Input: VTC receives raw audio files in .wav format as inputs. 

2. Output: The tool outputs an RTTM (rich transcription time marked) file with turn takes and time stamps for every audio file it processes (named according to the filename of the audio file), and one rttm.csv file that contains the speaker segments from all files. Find more information about rttm files in this [stack overflow entry](https://stackoverflow.com/questions/30975084/rttm-file-format).

3. Parameters: The tool receives the following arguments (required arguments are indicated with "!")
    - ! wavs: path to the directory containing the audio files
    - ! output: path to the directory where outputs will be stored (must exist)
    - device: on which computing device the tool runs, either cpu, mps, gpu or cuda, and it is by default set to gpu
    - min_duration_on_s: deletes utterances shorter than this threshold during post-processing
    - min_duration_off_s: fills gaps smaller than this threshold between utterances of the same speaker group during post-processing
    - checkpoint: which model checkpoint to use, by default set to the most recent one
    - batch_size: how many samples to process at a time, by default set to 128
    - recursive_search: searches recursively for files in waves directory (needed if your data is located in nested subdirectories)
    - high_precision: sets higher higher thresholds for speech detection during inference
    - keep_raw: saves raw (==non-post-processed) outputs to disk

4. Code: To run VTC with default settings on CPU, run this code from VTC directory::

```bash
cd ~/LONGFORM_TOOLS/VTC						# in case you are not in VTC directory, navigate there
uv run scripts/infer.py --wavs ../LongformWorkshop26/data/recordings/wav --output ../LongformWorkshop26/data/results/VTC_outputs --device cpu
```

Alternatively, you can specify inputs and additional parameters in the bash script that VTC is providing in VTC/scripts/run.sh. For an example, see this repository's examples/VTC_script_example.sh file. 

If you are familiar with Praat or Elan, you can use the rttm_to_eaf_textgrid converter to inspect the results. Note that you need to have conda installed to run the code, and that the argument audio-path is not required, so you may delete it.

```bash
cd ~/LONGFORM_TOOLS/LongformWorkshop26
conda env create -f code/environment.yml	# if you lack conda, refer to technical_setup_mac_linux!
conda activate longforms                    
python code/rttm_to_eaf_textgrid.py data/results/VTC_outputs/rttm.csv --audio-path data/recordings/wav --output-path data/annotations/VTC_annotations
conda deactivate
```

### Child speech analysis I: Speech maturity classification

The [Speech Maturity Model](https://github.com/arxaqapi/speech-maturity) classifies infant vocalizations as non-canonical (NON-CAN) or canoncical (CAN) babbling, laughing (LAU), crying (CRY), with an additional class for everything else (JUNK).

```bash
cd ~/LONGFORM_TOOLS
mkdir -p LongformWorkshop26/data/results/Speech_Maturity_outputs
git clone --recurse-submodules https://github.com/arxaqapi/speech-maturity.git
cd speech-maturity
uv sync
```

1. Input: The tool receives audio clips that contain child vocalizations, f.ex., extracted via VTC.
2. Output: The tool returns a .csv file with the columns id, predicted_label (integer from 0 to 4), and corresponding prediction_class_name.
3. Parameters: 
	The following paths need to be set inside the file run.sh that you can find in speech-maturity directory:

    - ! audios_path: path to VTC segments, set to ~/LONGFORM_TOOLS/LongformWorkshop26/data/recordings/VTC_segments/KCHI 
    - ! output_folder: where to store the results, set to ../LongformWorkshop26/data/results/Speech_Maturity_outputs
    
    In addition, we need to set a few parameters in the file "hparams/hparams.yaml", in section test_dataloader_options:

    - ! batch_size: how many samples to run inference on at once; set to 4 if you use the example data, or to a reasonable small size such that: amount of data % batch_size == as small as possible
    - ! num_workers: paralellization mode during data loading; set to 0
    - ! drop_last: whether to drop the last data samples resulting from data % batchsize; set to "True"

4. Code: Before we can run the tool, we need to chunk the long-form audio into utterances based on the VTC outputs. We prepared a small script for that, which requires the conda environment from technical_setup_mac_linux file:

```bash
cd ~/LONGFORM_TOOLS/LongformWorkshop26					
conda activate longforms					# if this command fails, refer to technical_setup and install conda environment
python code/extract_segments.py	--kchi		# extracts KCHI vocalizations only
```

Now we navigate back to speech-maturity directory and execute the script that runs the tool:

```bash
cd ~/LONGFORM_TOOLS/speech-maturity			# in case you are not in speech-maturity directory, navigate there
bash run.sh
```

### Child speech analysis II: Babbling recognition

[BabAR](https://github.com/MarvinLvn/BabAR) has VTC already included as the first step in its pipeline. Therefore, it has the same requirements as VTC.

```bash
cd ~/LONGFORM_TOOLS											
mkdir -p LongformWorkshop26/data/results/BabAR_outputs		# create output folder 
git clone --recurse-submodules https://github.com/MarvinLvn/BabAR.git
cd BabAR
uv sync
```

1. Input: Like VTC, BabAR receives 16kHz mono-channel .wav files.

2. Output: The tool returns both the outputs of VTC, and .csv files with predicted phonemes for key-child vocalizations (KCHI classified utterances by VTC).

3. Parameters: 

    - ! wavs: path to the recordings
    - ! output: path to output folder
    - ! device: device to run the model on: cpu, mps (macOS only), gpu or cuda
    - batch_size: how many samples to process at once during inference with BabAR
    - vtc_batch_size: how many samples to process at once during inference with VTC
    - checkpoint: which model checkpoint to load
    - vocab_phoneme_path: path to .json file containing phoneme vocabulary
    - context_duration: context window for inference with BabAR
    - num_workers: paralellization for data loading
    - max_utt_dur: maximum duration of an utterance in seconds
    - high_precision: VTC parameter
    - transcribe_och: whether to transcribe OCH (other child) vocalizations as well; default is to key-child (KCHI) only

4. Code: 

```bash
cd ~/LONGFORM_TOOLS/BabAR					# in case you are not in BabAR directory, navigate there
uv run src/pipeline.py --wavs ../LongformWorkshop26/data/recordings/wav --output ../LongformWorkshop26/data/results/BabAR_outputs --device cpu
```

### Caregiver speech analysis: Word count estimation

The [Automatic Linguistic Unit Count Estimater](https://github.com/orasanen/ALICE) (ALICE) uses VTC and [SylNet](https://github.com/shreyas253/SylNet) in its pipeline. The tool estimates the number of linguistic units in utterances from adult speakers only (FEM and MAL classes by VTC). 

Note that it relies on an older version of VTC, and that users with Apple Silicon devices need to execute a few extra commands, as shown below:

```bash
cd ~/LONGFORM_TOOLS
git clone --recurse-submodules https://github.com/orasanen/ALICE.git
cd ALICE
conda env create -f ALICE_Linux.yml         # for Linux / WSL users
conda env create -f ALICE_macOS.yml         # for macOS users (non Apple Silicon processors)
# the following commands concern Apple Silicon devices only:
CONDA_SUBDIR=osx-64 conda env create -f ALICE_macOS.yml
conda activate ALICE
conda config --env --set subdir osx-64
```

1. Input: As the tool relies on VTC, it receives 16kHz mono-channel .wav audio files as input.
2. Output: The tool outputs one .txt file with estimations for the number of phonemes, syllables, and words per input file, and one .txt file for each audio file where the rows correspond to speaker utterances. It also saves the VTC outputs in one .rttm file.
3. Parameters: ALICE only has positional arguments (those are not named but rather read by the tool depending on their position in the command)

    - first positional argument: path to the recordings, or to a .txt file with a list of .wav paths (one path per row)
    - second positional argument: "gpu", if the dara should be processed on gpu

    Note that we cannot specify the output folder path, so results will be stored inside ALICE folder.

4. Code: We need to active ALICE environment with required software packages before running the tool:

```bash
cd ~/LONGFORM_TOOLS/ALICE					# in case you are not in ALICE directory, navigate there
conda activate ALICE                       
./run_ALICE.sh ../LongformWorkshop26/data/recordings/wav/
conda deactivate 
```

## Further information

Here you can find links to interesting material and references.

### Useful links

- [PHRP training](https://phrptraining.com)
- [ACLEW tutorials](https://osf.io/b2jep/overview)
- minCHAT format checker [upload procedure](https://github.com/aclew/AAS-minCHAT-Checker/blob/master/README.md) 
- [minCHAT checker](https://aclew.shinyapps.io/AAS-minCHAT-Checker/) 
- gold standard [test submission](https://aclew.shinyapps.io/GSCompareApp/) 
- Elan software [download](https://archive.mpi.nl/tla/elan/download) and [documentation](https://www.mpi.nl/tools/elan/docs/manual/index.html)

### References

```bibtex
@misc{charlot_babyhubert_2025,
	title = {{BabyHuBERT}: {Multilingual} {Self}-{Supervised} {Learning} for {Segmenting} {Speakers} in {Child}-{Centered} {Long}-{Form} {Recordings}},
	shorttitle = {{BabyHuBERT}},
	url = {http://arxiv.org/abs/2509.15001},
	doi = {10.48550/arXiv.2509.15001},
	urldate = {2025-10-04},
	publisher = {arXiv},
	author = {Charlot, Théo and Kunze, Tarek and Poli, Maxime and Cristia, Alejandrina and Dupoux, Emmanuel and Lavechin, Marvin},
	month = sep,
	year = {2025},
}

@inproceedings{lavechin_open-source_2020,
	title = {An {Open}-{Source} {Voice} {Type} {Classifier} for {Child}-{Centered} {Daylong} {Recordings}},
	url = {https://www.isca-archive.org/interspeech_2020/lavechin20_interspeech.html},
	doi = {10.21437/Interspeech.2020-1690},
	urldate = {2025-10-24},
	booktitle = {Interspeech 2020},
	publisher = {ISCA},
	author = {Lavechin, Marvin and Bousbib, Ruben and Bredin, Hervé and Dupoux, Emmanuel and Cristia, Alejandrina},
	month = oct,
	year = {2020},
	pages = {3072--3076},
}

@misc{lavechin_babar_2026,
	title = {{BabAR}: from phoneme recognition to developmental measures of young children's speech production},
	shorttitle = {{BabAR}},
	url = {http://arxiv.org/abs/2603.05213},
	doi = {10.48550/arXiv.2603.05213},
	urldate = {2026-09-06},
	publisher = {arXiv},
	author = {Lavechin, Marvin and Bergelson, Elika and Levy, Roger},
	month = jun,
	year = {2026},
}

@article{rasanen_alice_2021,
	title = {{ALICE}: {An} open-source tool for automatic measurement of phoneme, syllable, and word counts from child-centered daylong recordings},
	volume = {53},
	url = {https://link.springer.com/10.3758/s13428-020-01460-x},
	doi = {10.3758/s13428-020-01460-x},
	number = {2},
	urldate = {2025-11-06},
	journal = {Behavior Research Methods},
	author = {Räsänen, Okko and Seshadri, Shreyas and Lavechin, Marvin and Cristia, Alejandrina and Casillas, Marisa},
	month = apr,
	year = {2021},
	pages = {818--835},
}

@misc{vandam_corpus_2018,
	title = {VanDam Public Daylong HomeBank Corpus},
	url = {https://gin.g-node.org/LAAC-LSCP/vandam-data/src/master},
	doi = {doi:10.21415/T5388S},
	author = {VanDam, Mark},
	year = {2018}
}


@article{vandam_homebank_2016,
	title = {{HomeBank}: {An} {Online} {Repository} of {Daylong} {Child}-{Centered} {Audio} {Recordings}},
	volume = {37},
	issn = {0734-0478, 1098-9056},
	shorttitle = {{HomeBank}},
	url = {http://www.thieme-connect.de/DOI/DOI?10.1055/s-0036-1580745},
	doi = {10.1055/s-0036-1580745},
	number = {02},
	urldate = {2025-10-15},
	journal = {Seminars in Speech and Language},
	author = {VanDam, Mark and Warlaumont, Anne and Bergelson, Elika and Cristia, Alejandrina and Soderstrom, Melanie and De Palma, Paul and MacWhinney, Brian},
	month = apr,
	year = {2016},
	pages = {128--142},
}


@inproceedings{zhang_employing_2025,
	title = {Employing self-supervised learning models for cross-linguistic child speech maturity classification},
	url = {https://www.isca-archive.org/interspeech_2025/zhang25r_interspeech.html},
	doi = {10.21437/Interspeech.2025-1946},
	urldate = {2026-08-08},
	booktitle = {Interspeech 2025},
	publisher = {ISCA},
	author = {Zhang, Theo and Suresh, Madurya and Warluamont, Anne and Hitczenko, Kasia and Cristia, Alejandrina and Cychosz, Margaret},
	month = aug,
	year = {2025},
	pages = {2825--2829},
}
```
