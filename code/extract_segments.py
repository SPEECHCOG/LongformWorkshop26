import os
import glob
import argparse
import pandas as pd
from tqdm import tqdm
from typing import List
import soundfile as sf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Chunk audio files according to VTC outputs.')
    parser.add_argument('-r', '--rttm_path', default='data/results/VTC_outputs/rttm.csv', help='RTTM CSV file')
    parser.add_argument('-a', '--audio_path', default='data/recordings', help='Directory containing wav files')
    parser.add_argument('-o', '--output_path', default='data/recordings/VTC_segments', help='Output directory')
    parser.add_argument('-k', '--kchi', required=False, action='store_true', help='Inlcude KCHI vocalizations')
    parser.add_argument('-c', '--chi', required=False, action='store_true', help='Inlcude OCH vocalizations')
    parser.add_argument('-f', '--fem', required=False, action='store_true', help='Inlcude FEM utterances')
    parser.add_argument('-m', '--mal', required=False, action='store_true', help='Inlcude MAL utterances')
    return parser.parse_args()

def main():
    args = parse_args()

    #--- read VTC outputs
    df = pd.read_csv(args.rttm_path)

    #--- which speakers to include
    speakers = []
    if args.kchi:
        speakers.append('KCHI')
    if args.chi:
        speakers.append('OCH')
    if args.fem:
        speakers.append('FEM')
    if args.mal:
        speakers.append('MAL')
    if len(speakers) == 0:
        print(f'No speakers chosen! Run script again using at least one of the following flags: --kchi --chi --fem --mal')

    #--- iterate over VTC annotations and chunk audio
    for name, group in df.groupby('uid'):
        wav_path = os.path.join(args.audio_path, f'{name}.wav')
        if not os.path.isfile(wav_path):
            print(f'File not found: {wav_path}')
            continue

        print(f'Processing file: {name}')
        y, sr = sf.read(wav_path)

        for _, row in tqdm(group.iterrows(), total=len(group), desc='Segments', leave=False):
            speaker = row['label']
            if not speaker in speakers:
                continue
            onset = row['start_time_s']
            duration = row['duration_s']
            start_sample = int(onset * sr)
            end_sample = int((onset + duration) * sr)
            y_segment = y[start_sample:end_sample]
            if len(y_segment) == 0:
                continue

            segment_folder = os.path.join(args.output_path, str(speaker))
            os.makedirs(segment_folder, exist_ok=True)
            onset_ms = int(onset * 1000)
            duration_ms = int(duration * 1000)
            out_file = os.path.join(segment_folder, f'{name}_{speaker}_{onset_ms}_{duration_ms}.wav')
            sf.write(out_file, y_segment, sr)


if __name__ == '__main__':
    main()

#EOF