#!/usr/bin/env python3

import argparse
import pandas as pd
from pathlib import Path
import pympi
from typing import Dict, List, Optional
import wave


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convert RTTM CSV to TextGrid and EAF.')
    parser.add_argument('rttm_path', help='RTTM CSV file')
    parser.add_argument('-a', '--audio-path', default=None, help='Directory containing wav files')
    parser.add_argument('-o', '--output-path', required=True, help='Output directory')
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rttm_path = Path(args.rttm_path)
    output_dir = Path(args.output_path)
    audio_dir = Path(args.audio_path) if args.audio_path else None

    assert rttm_path.is_file(), f'RTTM file does not exist: {rttm_path.resolve()}'
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_info = get_audio_info(audio_dir)
    data = read_rttm_csv(rttm_path)

    for uid, annotations in data.groupby('uid'):
        process_recording(
            uid=uid,
            annotations=annotations,
            audio_info=audio_info,
            output_dir=output_dir
        )


def get_audio_info(audio_dir: Optional[Path]) -> Dict[str, Dict[str, float | str]]:
    if audio_dir is None:
        return {}
    wav_files = {}
    for wav_path in audio_dir.rglob('*.wav'):
        try:
            with wave.open(str(wav_path), 'rb') as wav:
                duration = wav.getnframes() / wav.getframerate()
            wav_files[wav_path.stem] = {
                'path': str(wav_path.resolve()),
                'duration': duration
            }
        except Exception as exc:
            print(f'Failed to read {wav_path}: {exc}')
    return wav_files


def read_rttm_csv(rttm_path: Path) -> pd.DataFrame:
    data = pd.read_csv(rttm_path, sep=',')
    data['end_time_s'] = data['start_time_s'] + data['duration_s']
    return data


def create_textgrid(
    annotations: pd.DataFrame,
    wav_path: str,
    duration: float,
    output_file: Path
) -> None:
    tg = pympi.TextGrid(xmax=duration)
    for tier_name, tier_df in annotations.groupby('label'):
        tg.add_tier(tier_name)
        for _, row in tier_df.iterrows():
            tg.get_tier(tier_name).add_interval(
                float(row['start_time_s']),
                float(row['end_time_s']),
                tier_name
            )
    tg.to_file(str(output_file))


def create_eaf(
    annotations: pd.DataFrame,
    wav_path: str,
    duration: float,
    output_file: Path
) -> None:
    eaf = pympi.Elan.Eaf()
    eaf.add_linked_file(
        file_path=wav_path,
        relpath=wav_path,
        mimetype='audio/x-wav'
    )
    for tier_name, tier_df in annotations.groupby('label'):
        eaf.add_tier(tier_name)
        for _, row in tier_df.iterrows():
            eaf.add_annotation(
                tier_name,
                int(round(row['start_time_s'] * 1000)),
                int(round(row['end_time_s'] * 1000)),
                tier_name
            )
    eaf.to_file(str(output_file))


def get_recording_info(
    uid: str,
    annotations: pd.DataFrame,
    audio_info: Dict[str, Dict[str, float | str]]
) -> tuple[str, float]:
    wav_path = f'{uid}.wav'
    duration = float(annotations['end_time_s'].max())
    if uid in audio_info:
        wav_path = str(audio_info[uid]['path'])
        duration = float(audio_info[uid]['duration'])
    return wav_path, duration


def process_recording(
    uid: str,
    annotations: pd.DataFrame,
    audio_info: Dict[str, Dict[str, float | str]],
    output_dir: Path
) -> None:
    wav_path, duration = get_recording_info(uid, annotations, audio_info)

    textgrid_file = output_dir / f'{uid}.TextGrid'
    eaf_file = output_dir / f'{uid}.eaf'

    create_textgrid(
        annotations=annotations,
        wav_path=wav_path,
        duration=duration,
        output_file=textgrid_file
    )

    create_eaf(
        annotations=annotations,
        wav_path=wav_path,
        duration=duration,
        output_file=eaf_file
    )

if __name__ == '__main__':
    main()