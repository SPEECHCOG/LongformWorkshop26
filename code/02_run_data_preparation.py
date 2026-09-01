#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Kerstin Markl (BlindeEule) and Daniil Kocharov (dan_ya)
@info: This script serves to prepare the VanDam data as reference annotations. Code enhancement by Microsoft Copilot. 
"""

import os
import numpy as np
import pandas as pd
import soundfile as sf
from tqdm import tqdm
from utils import recursive_glob,  map_speaker_to_group, map_vcm_to_full_terms
tqdm.pandas()


def main():

    #--- tool variables
    # TODO: make these overwritable via config file --> participants can play with parameters
    MIN_DURATION_ON_S = 0.1             # VTC parameter
    MIN_DURATION_OFF_S = 0.1            # VTC parameter
    MAX_LEN = 9217                      # Speech Maturity parameter

    #--- in-paths
    csvs = recursive_glob(directory='data/vandam-data/annotations/eaf/converted', file_ending='csv', recursive=False)
    wavs = recursive_glob(directory='data/vandam-data/recordings/converted/standard', file_ending='wav')

    #--- out-paths
    vtc_out_dir = 'results/reference_speaker_types'
    sm_out_dir = 'results/reference_speech_maturity'
    audio_snippets_out = os.path.join(sm_out_dir, 'infant_vocalizations')
    other_files_out = os.path.join(sm_out_dir, 'tables')
    os.makedirs(vtc_out_dir, exist_ok=True)
    os.makedirs(sm_out_dir, exist_ok=True)
    os.makedirs(audio_snippets_out, exist_ok=True)
    os.makedirs(other_files_out, exist_ok=True)
    all_sm_csv_path = os.path.join(other_files_out, 'vcm_labels.csv')
    all_sm_json_path = os.path.join(other_files_out, 'vcm_labels.json')
    all_vtc_csv_path = os.path.join(vtc_out_dir, 'rttm.csv')

    #--- find corresponding wave and csv files
    wave_df = pd.DataFrame({'wavepath': wavs})
    csv_df = pd.DataFrame({'csvpath': csvs})
    wave_df['raw_filename'] = wave_df['wavepath'].apply(lambda x: os.path.basename(x).split('.')[0])
    csv_df['filename'] = csv_df['csvpath'].apply(lambda x: os.path.basename(x).split('.')[0])
    csv_df['raw_filename'] = csv_df['filename'].apply(lambda x: x.split('_')[:2])
    data = csv_df.merge(wave_df, how='left', on='raw_filename')
    print(f'found the following annotations: {data[['raw_filename', 'filename']]}')

    #--- data structures
    vtc_dfs = []
    vcm_dfs = []
    vcmLabels = []

    #--- conversion
    print(f'starting data conversion...')
    for i, row in tqdm(data.iterrows()):
        #--- df variables
        csvpath = row['csvpath']
        wavepath = row['wavepath']
        filename = row['filename']
        raw_filename = row['raw_filename']

        #--- try to read csv
        try:
            df = pd.read_csv(csvpath, keep_default_na=False)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()

        #--- extract annotations in Voice Type Classifier output style   
        if len(df) == 0:
            rttm = df
        else:
            rttm = convert_columns_to_VTC_format(df)
            rttm = merge_annotations(df_a=rttm, min_duration_on_s=MIN_DURATION_ON_S, 
                                     min_duration_off_s=MIN_DURATION_OFF_S)
            vtc_dfs.append(rttm)

        #--- slice audio clips according to Voice Type Classifier expectations
        # TODO: just slice according to the annotation timestamps to match VTC output data structures

        #--- write Voice Type Classifier style data to csv
        out_path_dir_vtc = os.path.join(vtc_out_dir, raw_filename)
        out_path_file_vtc = os.path.join(out_path_dir_vtc, f'{filename}.rttm')
        os.makedirs(out_path_dir_vtc, exist_ok=True)
        write_df_to_rttm(df=rttm, outpath=out_path_file_vtc)

        #--- extract annotations in Speech Maturity Classifier output style
        if 'vcm' in df.columns:
            vcm_df = df.copy()
            vcm_df.dropna(subset=['vcm'], inplace=True)
            vcm_df = vcm_df[vcm_df['vcm'].isin(['N', 'C', 'Y', 'L'])]
            vcm_dfs.append(vcm_df)
            vcmLabels.extend(vcm_df.vcm.to_list())

        #--- slice & pad audio clips according to Speech Maturity Classifier expectations
        if not os.path.exists(wavepath):
            print(f'File not found: {wavepath}')
            continue
        vcm_df = extract_vcm_clips(df=vcm_df, wavepath=wavepath, out_path=audio_snippets_out, max_len=MAX_LEN)
        vcm_dfs.append(vcm_df)

    #--- write one additional file for all Voice Type Classifier data
    all_vtc_data = pd.concat(vtc_dfs, axis=0, ignore_index=True)
    all_vtc_data.sort_values(by=['uid', 'start_time_s'], inplace=True)
    print(f'number of utterances from all speaker groups in the data set: {len(all_vtc_data)}')
    all_vtc_data.to_csv(all_vtc_csv_path, index=False)

    #--- write one additional file for all Speech Maturity Classifier data
    # TODO: write vcm_dfs to json and csv

#--------------------------------------------------------------------------------------

def convert_columns_to_VTC_format(df: pd.DataFrame) -> pd.DataFrame:
    '''
        method converts a data frame to match the .csv output file from VTC 2.0. 
        args: 
            df (pd.DataFrame): columns 'uid', 'speaker', 'onset', 'duration', 'transcription'
        returns: 
            df (pd.DataFrame): columns 'uid', 'label', 'start_time_s, duration_s, end_time_s
    '''
    # TODO: check label or whats the column names
    # TODO: apply map_speaker_to group
    df = df.copy()
    df = df[['uid', 'onset', 'duration', 'speaker']]
    df['speaker'] = df['speaker'].apply(lambda x: map_speaker_to_group(x))
    df['onset'] = df['onset'] / 1000
    df['duration'] = df['duration'] / 1000
    df.rename(columns={'onset': 'start_time_s',
                       'duration': 'duration_s',
                       'speaker': 'label'}, inplace=True)
    return df


def extract_vcm_labels(df: pd.DataFrame) -> pd.DataFrame:
    #--- THIS METHOD EXTRACTS UTTERANCES WITH VCM FROM A DF AND DROPS THE REST OF THE ROWS
    """
        df (pd.DataFrame): expected columns: speaker, uid, onset, duration
        returns: empty df or df with columns speaker, uid, onset, duration, vcm
    """
    df = df.copy()
    if len(df) == 0:
        return df
    if 'vcm' not in df.columns:
        return pd.DataFrame()
    df['speaker'] = df['speaker'].apply(lambda x: map_speaker_to_group(x))
    allowed_speakers = ['KCHI']
    df = df[df['speaker'].isin(allowed_speakers)]
    df = df[['uid', 'speaker', 'onset', 'duration', 'vcm']]
    return df


def extract_vcm_clips(df: pd.DataFrame, wavepath: str, out_path: str, max_len: int) -> pd.DataFrame:
    #--- THIS METHOD EXTRACTS INFANTS' VOCALIZATIONS FROM AUDIO CLIPS, 0-PADS AND WRITED THEM TO OUT_PATH
    """
        df (pd.DataFrame): expected columns: speaker, uid, onset (ms), duration (ms), vcm
        wavepath: path to audio file
        out_path: where to store the clips
        max_len: max length of the audio arrays in int == 9217 (according to paper Zhang et al.:
            Employing self-supervised learning models for cross-linguistic child speech  maturity classification)
    """
    #--- read stuff
    df = df.copy()

    if len(df) == 0:
        pass

    cwd = os.getcwd()
    uid = os.path.basename(wavepath).split('.')[0]
    y, sr = sf.read(wavepath, samplerate=None)
    #info = sf.info(wavepath)
    filenames = []
    filepaths = []
    labels = []

    for i, row in df.iterrows():
        #--- slicing
        speaker = row['speaker']
        label = row['vcm']
        start_voc = int(row['onset'] * (sr/1000))
        duration_voc = int(row['duration'] * (sr/1000))
        end_voc = int((row['onset'] + row['duration']) * (sr/1000))
        voc_segment = y[start_voc:end_voc]
        if len(voc_segment) == 0:
            continue

        #--- chunk slicing to meet max_len criteria and not throw away so much data
        n_chunks = int(np.ceil(len(voc_segment) / max_len))
        for chunk_idx in range(n_chunks):
            chunk_start = chunk_idx * max_len
            chunk_end = min((chunk_idx + 1) * max_len, len(voc_segment))
            chunk = voc_segment[chunk_start:chunk_end]

            #--- padding
            len_pads = max_len - len(chunk)
            if len_pads == 0:
                before = after = 0
            elif len_pads % 2 == 0:
                before = after = len_pads//2
            else:
                before = len_pads//2
                after = len_pads - before
            chunk = np.pad(chunk, (before, after), 'constant', constant_values=(0, 0))
            assert len(chunk) == max_len

            #--- sample new position
            chunk_start_sample = start_voc + chunk_start
            padded_filename = (f'{uid}_{chunk_start_sample}_{speaker}_part{chunk_idx}')
            voc_out_path = os.path.join(out_path, f'{padded_filename}.wav')
            sf.write(voc_out_path, chunk, sr)
            filenames.append(padded_filename)
            filepaths.append(os.path.join(cwd, voc_out_path))
            labels.append(label)
    
    result = pd.DataFrame({'filenames': filenames, 'wav': filepaths, 'label': labels})
    return result


def merge_annotations(df_a: pd.DataFrame, min_duration_on_s: float, min_duration_off_s: float) -> pd.DataFrame:
    #--- THIS METHOD IMITATES VTC SETTINGS OF MERGING TOO SHORT OR TOO CLOSE ANNOTATIONS

    df = df_a.copy().reset_index(drop=True)
    if len(df) == 0 or len(df.columns) <= 1:
        return df
    if min_duration_on_s > 0.0:
        df = df[df['duration_s'] >= min_duration_on_s].reset_index(drop=True)
    if min_duration_off_s > 0.0:
        result = []
        i = 0
        while i < len(df):
            current = df.iloc[i].copy()
            j = i + 1
            while j < len(df):
                next_row = df.iloc[j]
                distance = (next_row['start_time_s'] - (current['start_time_s'] + current['duration_s']))
                if (current['label'] == next_row['label']and distance < min_duration_off_s):
                    current['duration_s'] += next_row['duration_s'] + distance
                    j += 1
                else:
                    break
            result.append(current)
            i = j
        df = pd.DataFrame(result).reset_index(drop=True)
    return df


def write_df_to_rttm(df: pd.DataFrame, outpath: str) -> None:
    '''
        writes dataframe object to .rttm format: SPEAKER <file-id> <channel> <start> <duration> <ortho> <stype> <name> <conf>
        args: 
            df (pd.DataFrame): dataframe containing at least the columns uid, onset, duration, speaker
            outpath (str): path where to save the file, ending with '.rttm'
    '''
    with open(outpath, 'w') as f:
        for _, r in df.iterrows():
            uid = r['uid']
            onset = r['start_time_s']
            duration = r['duration_s']
            speaker = r['label']
            line = (
                f'SPEAKER {uid} 1 '
                f'{onset} {duration} '
                f'<NA> <NA> {speaker} <NA> <NA>'
            )
            f.write(line + '\n')
    pass


if __name__=='__main__':
    main()

#AUSDIEMAUS