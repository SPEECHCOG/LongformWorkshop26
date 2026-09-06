# note: this script cannot be executed from the current directory and merely serves as an example
#       for you to set variables in the script VTC/scripts/run.sh

# replace DISK and USERNAME with your file structure. "~" makes the path relative to home directory
audios_path='~/DISK/USERNAME/LONGFORM_TOOLS/LongformWorkshop26/data/recordings'
output='~/DISK/USERNAME/LONGFORM_TOOLS/LongformWorkshop26/data/results/VTC_outputs'
mkdir -p $output

uv run scripts/infer.py \
    --wavs "$audios_path" \
    --output "$output" \
    --recursive_search \
    --device gpu \
    --keep_raw \
    --high_precision \
    --batch_size 64 \
    --min_duration_off_s 0.3 \
    --min_duration_on_s 0.3