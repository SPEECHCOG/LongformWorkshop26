#!/usr/bin/env bash

# note: this script can be executed from LongformWorkshop26 directory, with the command
#       bash examples/run_VTC_advanced.sh

#--- paths: ignore this ---
OS="$(uname -s)"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIRECTORY="$(cd -- "$SCRIPT_DIR/.." && pwd)"
PROJECT_DIR="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
VTC_DIR="$PROJECT_DIR/VTC"

AUDIO_DIR="$REPO_DIRECTORY/data/recordings"
OUTPUT_DIR="$REPO_DIRECTORY/data/results/VTC_outputs"
mkdir -p "$OUTPUT_DIR"

#--- navigation: ignore this ---
cd "$VTC_DIR" || exit 1
back() {
    cd $REPO_DIRECTORY
}
trap back EXIT

#--- extra commands for macOS users: ignore this ---
if [[ "$OS" == "Darwin" ]]; then
    echo "running on macOS"
    export PATH="/opt/homebrew/bin:$PATH"
    export DYLD_LIBRARY_PATH="/opt/homebrew/opt/ffmpeg@8/lib:${DYLD_LIBRARY_PATH:-}"
else
    echo "running on $OS"
fi

#--- variables: set this! ---           # we define variables here, then pass them to VTC below
device="cpu"                            # put mps if you're on macOS, gpu or cuda depending on your device
checkpoint="VTC-2/model/best.ckpt"      # which model checkpoint to use
min_duration_on_s="0.1"                 # deletes utterances shorter than this threshold during post-processing
min_duration_off_s="0.1"                # fills gaps smaller than this threshold between utterances of the same speaker group during post-processing


#--- boolean arguments: set this! ---
# to set boolean arguments, remove the "#" in front of the argument, and place them directly under the last executed argument
# make sure every line but the last one has a "\" sign in the end
# set "--recursive_search" if your audio data is in subfolders in recordings directory
# set "--high_precision" for higher thresholds for speech detection during inference
# set "--keep_raw" to save raw (==non-post-processed) outputs to disk


#--- run VTC: set this! --- 
uv run scripts/infer.py \
    --wavs "$AUDIO_DIR" \
    --output "$OUTPUT_DIR" \
    --device "$device" \
    --checkpoint "$checkpoint" \
    --min_duration_on_s "$min_duration_on_s" \
    --min_duration_off_s "$min_duration_off_s" #\
    #--high_precision #\
    #--recursive_search #\
    #--keep_raw




