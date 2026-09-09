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

## Miniconda installation
Anaconda, and its smaller version miniconda / miniforge are package manager tools. Navigate to the [Miniforge homepage](https://conda-forge.org/download/) and download the version that fits your device to Downloads folder. Run these commands, then follow the on-screen instructions and accept the default settings. Close and re-open your terminal afterwards.

```bash
bash ~/Downloads/Miniforge3-Linux-x86_64.sh             # miniforge for linux / WSL: download amd64 version
bash ~/Downloads/Miniforge3-Darwin-x86_64.sh            # miniforge for macOS (Intel)
bash ~/Downloads/Miniforge3-Darwin-arm64.sh             # miniforge for macOS (Apple Silicon)
```

In your terminal, you should now see "(base)" on the left before your username. Verify installation:

```bash
conda env list                              # should show the base environment
```

## Sound Exchange (SoX) installation
SoX is a software package for audio manipulation required for ALICE. 

```bash
sudo apt install sox                        # for wsl / linux only
brew install sox                            # for macOS only
sox --version
```

## git-lfs installation

Next, we install the version control git's large file system git-lfs. We assume you already have git installed. If this is not the case, jump to [git installation](#git-installation) first and then come back. 

```bash
sudo apt-get install git-lfs                # for wsl / linux users
git lfs install                             # for wsl / linux users
git-lfs install                             # for macOS users
```

The commands should output "Git LFS initialized."

### git installation
macOS comes with git preinstalled, yet wsl users might have to install it in their subsystem:

```bash
sudo apt-get install git                    # for wsl/linux users
git config --global user.name "myname"      # set your name
git config --global user.email "myemail"    # set your e-mail address
```

## FFmpeg installation
FFmpeg is a software for audio and video processing. Follow the instructions according to your OS.

### FFmpeg for macOS

```bash
brew install ffmpeg
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/ffmpeg@8/lib:$DYLD_LIBRARY_PATH"
python -c "import ctypes; ctypes.CDLL('/opt/homebrew/opt/ffmpeg@8/lib/libavcodec.dylib'); print('ok')"
```

### FFmpeg for linux / wsl

```bash
sudo apt install ffmpeg                       
ffmpeg -version
wget -qO- https://astral.sh/uv/install.sh | sh  # python package manager uv
ffmpeg -version
```

## uv installation
Last but not least, we install the Python package manager uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and re-open the terminal, then verify the installation:

```bash
uv --version
```
