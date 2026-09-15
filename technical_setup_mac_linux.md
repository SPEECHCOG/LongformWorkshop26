# Technical setup

Long-form tools require specific libraries installed on your device to work. In the following, we walk through the required installations step by step. In case you have a Windows device, please complete the steps in technical_setup_windows.md, then follow any of the steps in this tutorial using linux commands.

When running installation commands, you are usually prompted "install [...]. proceed? [y/n]" or similar. Answer by pressing y to proceed.

Here you can find steps to install: 
- [Miniconda](#miniconda-installation) needed for ALICE
- [Sox](#sound-exchange-sox-installation) needed for ALICE
- [git-lfs](#git-lfs-installation) needed for VTC, BAbar, Speech Maturity Classifier
- [FFmpeg](#ffmpeg-installation) needed for VTC, BAbar, Speech Maturity Classifier
- [uv](#uv-installation) needed for VTC, BAbar, Speech Maturity Classifier

NOTE: if you are on macOS, you need to install homebrew first before you can run the installations:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Close and re-open your terminal, then verify installation:

```bash
which brew
```

If you are running into errors, take a look at the [trouble shooting](#trouble-shooting) section:
- common error messages for [VTC](#common-error-messages-for-vtc)
- common error messages for [Speech Maturity Classifier](#common-error-messages-for-speech-maturity-classifier)

## Installation

### Miniconda installation
Anaconda, and its smaller version miniconda / miniforge are package manager tools. Navigate to the [Miniforge homepage](https://conda-forge.org/download/) and download the version that fits your device to Downloads folder. Run these commands, then follow the on-screen instructions and accept the default settings. Close and re-open your terminal afterwards.

```bash
# miniforge for linux / WSL: download amd64 version
bash ~/Downloads/Miniforge3-Linux-x86_64.sh
# miniforge for macOS (Intel)
bash ~/Downloads/Miniforge3-Darwin-x86_64.sh
# miniforge for macOS (Apple Silicon)
bash ~/Downloads/Miniforge3-Darwin-arm64.sh
```

In your terminal, you should now see "(base)" on the left before your username. Verify installation:

```bash
conda env list
```

### Sound Exchange (SoX) installation
SoX is a software package for audio manipulation required for ALICE. 

```bash
# for wsl / linux only
sudo apt install sox
# for macOS only                     
brew install sox
# for all                       
sox --version
```

### git-lfs installation

Next, we install the version control git's large file system git-lfs. We assume you already have git installed. If this is not the case, jump to [git installation](#git-installation) first and then come back. 

```bash
# for wsl / linux users
sudo apt-get install git-lfs
# for mac users
brew install git-lfs
# for all
git lfs install
```

The commands should output "Git LFS initialized."

### git installation
macOS comes with git preinstalled, yet wsl users might have to install it in their subsystem:

```bash
sudo apt-get install git
git config --global user.name "myname"
git config --global user.email "myemail"
```

### FFmpeg installation
FFmpeg is a software for audio and video processing. Follow the instructions according to your OS.

#### FFmpeg for macOS
NOTE: you need to run the last two lines every time before you run VTC, unless you add them to your .zshrc configuration file.

```bash
brew install ffmpeg@8
ls /opt/homebrew/opt/ffmpeg@8/lib/libav*
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/ffmpeg@8/lib:$DYLD_LIBRARY_PATH"
python -c "import ctypes; ctypes.CDLL('/opt/homebrew/opt/ffmpeg@8/lib/libavcodec.dylib'); print('ok')"
```

#### FFmpeg for linux / wsl

```bash
sudo apt install ffmpeg                       
ffmpeg -version
```

### uv installation
Last but not least, we install the Python package manager uv:

```bash
# wsl / linux users
curl -LsSf https://astral.sh/uv/install.sh | sh
# macOS
brew install uv                                 
```

Close and re-open the terminal, then verify the installation:

```bash
uv --version
```

## Trouble Shooting

DISCLAIMER: This repository serves as an easy introduction to long-form processing tools. We cannot take any responsibility for making the tools work on your devices. If you run into trouble that you cannot solve, please create an issue on the respective tool's GitHub page!

### Common error messages for VTC

1. "_pickle.UnpicklingError: invalid load key, 'v'."

This and related error messages can be raised when the model is not properly downloaded, which can be caused by git's large file system not being properly installed. The quickest fix is to install git-lfs, then remove and re-install the repository. 

NOTE: we will remove VTC repository permanantly - if you have any data stored there, save it outside the folder before you execute this code!

```bash
# for wsl / linux users
sudo apt-get install git-lfs
# for mac users
brew install git-lfs
# for all
git lfs install
cd ~/LONGFORM_TOOLS
rm -rf VTC
git clone --recurse-submodules https://github.com/LAAC-LSCP/VTC.git
cd VTC
uv sync	
```

2. "RuntimeError: Could not load libtorchcodec. Likely causes:
    1. FFmpeg is not properly installed in your environment. We support
        versions 4, 5, 6, 7, and 8.
    2. The PyTorch version (2.9.1) is not compatible with
        this version of TorchCodec. Refer to the version compatibility
        table:
        https://github.com/pytorch/torchcodec?tab=readme-ov-file#installing-torchcodec.
    3. Another runtime dependency; see exceptions below.
    [...]"

This error message can point to a missing or incompatible FFmpeg installation. Follow the steps for [FFmpeg installation above](#ffmpeg-installation), and rerun the tool.

3. "FileNotFoundError: [Errno 2] No such file or directory: '/[...]/LONGFORM_TOOLS/VTC/../LongformWorkshop26/data/results/VTC_outputs/raw_rttm'", and if you scroll a bit up, you might find 
"[ERROR] - (1/2) - File BN32_010007_part_1 could not be processed, skipping"
"[ERROR] - (2/2) - File BN32_010007_part_1 could not be processed, skipping"

Here, the audio files are not processed. This may be caused by a silent out-of-memory error, and can be mitigated by setting the flag "--batch_size 1" in the end of the command. If that does not solve the problem, your audio files might be corrupted.

### Common error messages for Speech Maturity Classifier

1. "AssertionError: Torch not compiled with CUDA enabled"

This message is raised when the script infer.py is trying to run speech maturity classification with default settings on CUDA (Compute Unified Device Architecture). Open infer.py script in speech maturity/scripts folder with a text editor. Navigate to ~line 313: 'run_opts["device"] = "cuda"  # cpu, cuda, mps', and change it to: run_opts["device"] = "cpu" # cpu, cuda, mps