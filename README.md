# Workshop on "Introduction to child-centered longform audio processing"

This repository is a step-by-step tutorial to use long-form analysis tools in practice. If you run into trouble with any of the tools, you might lack some of the required installations. In that case, refer to technical setup files in this repository.

Relevant sections for cloning this repo, install the example data, or convert your own data:

- [repository cloning](#repository-installation)
- [example data download](#example-data-download)
- [data conversion](#data-conversion)

Overview to run the tools:

- [Voice Type Classifier (VTC)](#speaker-diarization)
- [Speech Maturity Classifier](#child-speech-analysis-i-speech-maturity-classification)
- [Babbling Recognizer (BaBAR)](#child-speech-analysis-ii-babbling-recognition)
- [Linguistic Unit Count Estimation (ALICE)](#caregiver-speech-analysis-word-count-estimation)

If you use longform data analaysis tools for your research, please recognize the authors in the [references section](#references). You might want to check out our collection of [interesting links](#further-information).


## How to get started

We recommend to store all tools in one directory called LONGFORM_TOOLS. Open a terminal, and create the folder with these commands:

```bash
mkdir LONGFORM_TOOLS    # creates a new folder called "LONGFORM_TOOLS"
cd LONGFORM_TOOLS       # now we are in empty folder "LONGFORM_TOOLS"
ls                      # should yield an empty line
```

### Repository installation

In general, you can clone any public repository from Github by navigating to its homepage, clicking the green button "Code", copying the HTTPS-key and running "git clone HTTPS-link" (replace "HTTPS-link" with the actual link). Let's get started by cloning [this repository](https://github.com/SPEECHCOG/LongformWorkshop26):

```bash
git clone https://github.com/SPEECHCOG/LongformWorkshop26.git
```

### Example Data Download

TODO: add small script to slice 10min of data from VanDam

As example data, we use one recording plus annotations from the publically available [VanDam corpus](https://gin.g-node.org/LAAC-LSCP/vandam-data/src/master). Execute this code in your terminal from LONGFORM_TOOLS directory:

```bash
cd LongformWorkshop26                       
mkdir data
cd data
mkdir recordings
mkdir annotations
cd recordings
curl -L -O "https://gin.g-node.org/LAAC-LSCP/vandam-data/raw/master/recordings/converted/standard/BN32_010007.wav"
cd ../annotations
while read -r url; do curl -L -O "$url"; done < ../../code/annotation_links.txt
ls
cd ..
```

Note: If you would like to use your own data, please place it into the same folders to make the further pipelines work! The data directory is ignored by git, so your data will not be tracked by or transfered to Github.

### Data conversion 

TODO: include Daniil's data conversion script.

Most of the tools expect the recordings in .wav format with 16kHz samplingrate, and reference annotations in comma separated value format (.csv). To convert your data into expected formats (including audio extraction from video material), we prepared a script for you. Make sure your data is located in data/recordings and data/annotations folder, then execute the following lines in your terminal from LongformWorkshop26 directory:

```bash
conda env create -f code/environment.yml        # installs the conda environment in folder code
cd ..                                           # navigates back to LONGFORM_TOOLS directory
conda activate longforms                        # activate environment with required libraries
python code/convert_data.py                     # call the conversion script (it finds your data automatically)
```


## Long-form data processing

Let's get started with the actual data processing! Every section follows the structure: 1. input: what does the tool receive? 2. output: what does the tool return? 3. parameters: what parameters can be set to modify the tool outputs? 4. code: how to run the tool.

### Speaker diarization

The [Voice Type Classifier](https://github.com/LAAC-LSCP/VTC/tree/main) (VTC) determines who speaks when in an given audio file: It performs segmentation of the recording, classifying the segments where at least one speaker is active into the broad categories of female (FEM), male (MAL), key-child (KCH), and other children's (OCH) speech. Install the repository first:

```bash
git clone --recurse-submodules https://github.com/LAAC-LSCP/VTC.git
cd VTC
sh check_sys_dependencies.sh
uv sync
```

If one of the above commands fails, refer to technical_setup file and follow the installation steps required for VTC.

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
mkdir -p ../LongformWorkshop26/data/results
mkdir -p ../LongformWorkshop26/data/results/VTC_outputs
uv run scripts/infer.py --wavs ../LongformWorkshop26/data/recordings --output ../LongformWorkshop26/data/results/VTC_outputs --device cpu
# wait until the tool has finished, then navigate back
cd ..
```

    Alternatively, you can specify inputs and additional parameters in the bash script that VTC is providing in VTC/scripts/run.sh. For an example, see this repository's example/VTC_script_example.sh file. 

### Child speech analysis I: Speech maturity classification

The [Speech Maturity Model](https://github.com/arxaqapi/speech-maturity) classifies infant vocalizations as non-canonical (NON-CAN) or canoncical (CAN) babbling, laughing (LAU), crying (CRY), with an additional class for everything else (JUNK).

```bash
git clone --recurse-submodules https://github.com/arxaqapi/speech-maturity.git
cd speech-maturity
uv sync
```

1. Input: The tool receives audio clips that contain child vocalizations, f.ex., extracted via VTC.
2. Output: The tool returns a .csv file with the columns id, predicted_label (integer from 0 to 4), and corresponding prediction_class_name.
3. Parameters: 
    - ! wavs: path to the folder containing the audio files
    - ! predictions: path to the output folder
    - ! device: device to run the model on: cpu, mps (macOS only), gpu or cuda
    
    In addition, we need to set a few parameters in the file "hparams/hparams.yaml":

    - ! batch_size in test_dataloader_options: how many samples to run inference on at once; set to 1 if you use the example data, or a reasonable small size such that: amount of data % batch_size == as small as possible
    - ! num_workers: paralellization mode during data loading; set all 3 instances of "num_workers" to 0
    - ! drop_last: whether to drop the last data samples resulting from data % batchsize; set all 3 instaces to "True"

4. Code: Run this code from speech-maturity directory:

```bash
mkdir -p ../LongformWorkshop26/data/results
mkdir -p ../LongformWorkshop26/data/results/Speech_Maturity_outputs
uv run scripts/infer.py --wavs ../LongformWorkshop26/data/recordings --output ../LongformWorkshop26/data/results/Speech_Maturity_outputs --device cpu
cd ..
```

### Child speech analysis II: Babbling recognition

[BabAR](https://github.com/MarvinLvn/BabAR) has VTC already included as the first step in its pipeline. Therefore, it has the same requirements as VTC.

```bash
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
mkdir -p ../LongformWorkshop26/data/results
mkdir -p ../LongformWorkshop26/data/results/BabAR_outputs
uv run src/pipeline.py --wavs ../LongformWorkshop26/data/recordings --output ../LongformWorkshop26/data/results/BabAR_outputs --device cpu
```

### Caregiver speech analysis: Word count estimation

The [Automatic Linguistic Unit Count Estimater](https://github.com/orasanen/ALICE) (ALICE) uses VTC and [SylNet](https://github.com/shreyas253/SylNet) in its pipeline. The tool estimates the number of linguistic units in utterances from adult speakers only (FEM and MAL classes by VTC). Note that it relies on an older version of VTC.

```bash
git clone --recurse-submodules https://github.com/orasanen/ALICE.git
cd ALICE
conda env create -f ALICE_Linux.yml         # for Linux users
conda env create -f ALICE_macOS.yml         # for macOS users
```

1. Input: As the tool relies on VTC, it receives 16kHz mono-channel .wav audio files as input.
2. Output: The tool outputs one .txt file with estimations for the number of phonemes, syllables, and words per input file, and one .txt file for each audio file where the rows correspond to speaker utterances. It also saves the VTC outputs in one .rttm file.
3. Parameters: ALICE only has positional arguments (those are not named but rather read by the tool depending on their position in the command)

    - first positional argument: path to the recordings, or to a .txt file with a list of .wav paths (one path per row)
    - second positional argument: "gpu", if the dara should be processed on gpu

    Note that we cannot specify the output folder path, so results will be stored inside ALICE folder.

4. Code: We need to active ALICE environment with required software packages before running the tool:

```bash
conda activate ALICE                       
./run_ALICE.sh ../LongformWorkshop26/data/recordings
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
