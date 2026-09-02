# Workshop on "Introduction to child-centered longform audio processing"

Introduction. 
Overview to prepare your system for tool usage:

- [important notes for windows users](#windows-wsl-installation)
- [technical setup](#technical-setup)
- [tool downloads](#repository-installations)
- [example data download](#example-data-download)

Overview to run the tools:

- [data conversion](#data-conversion)
- [Voice Type Classifier (VTC)](#speaker-diarization)
- [Speech Maturity Classifier](#child-speech-analysis-i-speech-maturity-classification)
- [Babbling Recognizer (BaBAR)](#child-speech-analysis-ii-babbling-recognition)
- [Linguistic Unit Count Estimation (ALICE)](#caregiver-speech-analysis-word-count-estimation)

If you use longform data analaysis tools for your research, please recognize the authors in the [references section](#references). You might want to check out our collection of [interesting links](#further-information).

## How to get started
In this section, we walk you through necessary installations and downloads. Note that some commands vary depending on your operation system (mac / Linux / Windows). If you use a Windows system, please refer to the section [Windows WSL installation](#windows-wsl-installation), otherwise proceed to [technical setup](#technical-setup).

### Windows WSL installation
Many tools for long-form processing do not work for Windows systems. Therefore, we install the Windows Subsystem for Linux (WSL). Note that some of the following steps might require administrator rights. We are following the [official Windows tutorial for WSL installation](https://learn.microsoft.com/en-us/windows/wsl/install). 

1. Open PowerShell (if possible, in admin mode by right-clicking the icon and chosing 'Run as administrator'), type the following command and press enter: 

```bash
wsl --install
```

2. You will be prompted to set a UNIX password and username. Save these for later use! Then close the shell with the following command:

```bash
exit
```

3. You should now see a WSL shell icon on your desktop, or be able to find it from your search window. Open the WSL shell, or the PowerShell if you cannot find the icon. Verify the installation with the following command:

```bash
wsl                     # in case you are in PowerShell, this command switches to WSL system
wsl --version
```

4. The above command should output information about your Linux (Ubuntu) subsystem. If everything looks fine, proceed to the [technical setup](#technical-setup) and follow the instructions for linux users.

### Technical setup
In the following, we assume you have a macOS, Linux or WSL system. When running installation commands, you are usually prompted "install [...]. proceed? [y/n]" or similar. Answer by pressing y to proceed.

1. Open a terminal: on Mac, press Command + Spacebar, type terminal and press enter. On Linux, press Ctrl + Alt + T. On Windows double-click WSL or PowerShell icon, and run the following commands:

```bash
wsl                     # in case you are in PowerShell
ls                      # shows the current file system
```

2. Navigate to a folder where you want to store the tool repositories, replacing "myfolder" with your actual folder- or pathnames. Then we create a new folder in which we will store all the repositories and data.

```bash
cd myfolder             # navigates to folder called "myfolder" --> replace with your folder name!
cd ..                   # navigates back
cd myfolder/mysubfolder # navigates to subfolder called "mysubfolder"
mkdir LONGFORM_TOOLS    # creates a new folder called "LONGFORM_TOOLS"
cd LONGFORM_TOOLS       # now we are in empty folder "LONGFORM_TOOLS"
ls                      # should yield an empty line
```

3. Let's proceed with some system-wide requirements for the long-form tools. We start with miniconda. Run this command, then follow the on-screen instructions and accept the default settings. Close and re-open your terminal afterwards.

```bash
bash Miniforge3-latest-Linux-x86_64.sh      # miniconda for linux / WSL
bash Miniforge3-latest-MacOSX-x86_64.sh     # miniconda for macOS
```

4. (a) macOS users:

In your terminal, you should now see "(base)" on the left before your username. Verify the installation, then proceed to install package manager homewbrew:

```bash
conda env list                              # verify installation
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version                              # verify installation
```
Depending on your processor, you need to add homebrew to your path:

```bash
# for Apple Silicon users:
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile

# for Intel users:
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile
```

Next, we install the version control tool git and its large file system git-lfs using homebrew. Set your global variables and replace "myname" and "myemail" with your username or actual name and e-mail address:

```bash
brew install git
git --version                               # verify installation
git config --global user.name "myname"      # set your name
git config --global user.email "myemail"    # set your e-mail address
brew install git-lfs
git-lfs install
git lfs version                             # verify installation
```

Some more required packages, and we are (almost) done. Since ffmpeg caused trouble for us in the past, we need to export the path to the software and run some lines of verification, that should output "ok":

```bash
brew install sox                            # SoX for audio manipulation
brew install ffmpeg                         # FFmpeg for audio and video processing
ls /opt/homebrew/opt/ffmpeg@8/lib/libav*    # add the library to the path and verify
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/ffmpeg@8/lib:$DYLD_LIBRARY_PATH"
python -c "import ctypes; ctypes.CDLL('/opt/homebrew/opt/ffmpeg@8/lib/libavcodec.dylib'); print('ok')"
```

Last but not least, we install the Python package manager uv:

```bash
brew install uv
uv --version
````

4. (b) linux / WSL users:

In your terminal, you should now see "(base)" on the left before your username. Verify the installation, then proceed to install the version control tool git and its large file system git-lfs. Set your global variables and replace "myname" and "myemail" with your username or actual name and e-mail address:

```bash
conda env list                              # should show the base environment
sudo apt-get install git                    
git config --global user.name "myname"      # set your name
git config --global user.email "myemail"    # set your e-mail address
sudo apt-get install git-lfs
git lfs install
```

Some more packages required, and we are (almost) done.

```bash
sudo apt install sox                            # SoX for audio manipulation
sox --version
sudo apt install ffmpeg                         # FFmpeg for audio and video processing
ffmpeg -version
wget -qO- https://astral.sh/uv/install.sh | sh  # python package manager uv
```

### Repository installations
Now we are all set and can proceed to install the actual tools. Make sure you are inside folder "LONGFORM_TOOLS" (you can see it on the lefthand in your shell) before running the following commands. In general, you can clone any public repository from Github by navigating to its homepage, clicking the green button "Code", copying the HTTPS-key and running:

```bash
git clone HTTPS-link                        # replace "HTTPS-link" with the actual link
```

This will create a folder in your current directory with the contents of the repository. Yet, we are not done by simply cloning; we also need to install the tools' requirements. Let's get started by cloning this repository:

1. [LongformWorkshop26](https://github.com/SPEECHCOG/LongformWorkshop26)

Different tools require different software libraries, installed with package managers. In this repository, we rely on miniconda that we installed earlier:

```bash
git clone https://github.com/SPEECHCOG/LongformWorkshop26.git
cd LongformWorkshop26                       # navigate to repository folder
conda env create -f code/environment.yml    # installs the conda environment in folder code
cd ..                                       # navigates back to LONGFORM_TOOLS directory
```

2. [Voice Type Classifier](https://github.com/LAAC-LSCP/VTC/tree/main)

Some repositories have linked repositories called submodules. In this case, we need to initialize those before installing the requirements. 

```bash
git clone https://github.com/LAAC-LSCP/VTC.git
cd VTC
git submodule update --init --recursive     # initialize linked repositories
./check_sys_dependencies.sh                 # check system dependencies with script from the repo
uv sync                                     # install tool requirements using uv manager
cd ..
```

3. [Speech Maturity Classifier](https://github.com/arxaqapi/speech-maturity)

Instead of initializing submodules after cloning the repository, we can also set a flag for the git clone command:

```bash
git clone --recurse-submodules https://github.com/arxaqapi/speech-maturity.git
cd speech-maturity
uv sync
cd ..
```

4. [Babbling Automatic Recognition](https://github.com/MarvinLvn/BabAR)

```bash
git clone https://github.com/MarvinLvn/BabAR.git
cd BabAR
git submodule update --init --recursive 
uv sync
cd ..
```

5. [Automatic Linguistic Unit Count Estimation](https://github.com/orasanen/ALICE)

```bash
git clone --recurse-submodules https://github.com/orasanen/ALICE.git
cd ALICE
conda env create -f ALICE_Linux.yml         # for Linux users
conda env create -f ALICE_macOS.yml         # for macOS users
cd ..
```

### Example Data Download

As example data, we use one recording plus annotations from the publically available [VanDam corpus](https://gin.g-node.org/LAAC-LSCP/vandam-data/src/master). Execute this code in your terminal from LONGFORM_TOOLS directory:

```bash
cd LongformWorkshop26
mkdir data
cd data
mkdir recordings
mkdir annotations
cd recordings
curl -L -O "https://gin.g-node.org/LAAC-LSCP/vandam-data/src/master/recordings/converted/standard/BN32_010007.wav"
cd ../annotations
while read -r url; do curl -L -O "$url"; done < ../../code/annotation_links.txt
ls
cd ..
```

Note: If you would like to use your own data, please place it into the same folders to make the further pipelines work! The data directory is ignored by git, so your data will not be tracked by or transfered to Github.

You may now proceed to [long-form data processing section](#long-form-data-processing).



## Long-form data processing

Let's get started with the actual data processing! If you are using the example data, you may skip the first section.

### Data conversion

Most of the tools expect the recordings to be in .wav format with 16kHz samplingrate, and annotations to be in comma separated value format (.csv). To convert your data into expected formats (including audio extraction from video material), we prepared a script for you. Make sure your data is located in data/recordings and data/annotations folder, then execute the following lines in your terminal from LongformWorkshop26 directory:

```bash
conda activate longforms                        # activate environment with required libraries
python code/convert_data.py                     # call the conversion script (it finds your data automatically)
```

### Speaker diarization

- VTC + bash script

### Child speech analysis I: Speech maturity classification
- script to slice and throw away non-CHI for speech maturity

### Child speech analysis II: Babbling recognition
- BaBar

### Caregiver speech analysis: Word count estimation
- ALICE

## Further information
Here you can find links to interesting material and references.

### Useful links

- ACLEW tutorials
- minCHAT format checker
- ACLEW gold standard testing tool
- Elan documentation

### References

Corresponding papers to tools.