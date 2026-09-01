#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Kerstin Markl (BlindeEule), Daniil Kocharov (dan_ya)
@info: Common methods for scripts. Mapping methods are partially adopted from the ChildProject code basis.
"""

import os
import glob
from typing import List
from collections import defaultdict

def recursive_glob(directory: str, file_ending:str, recursive:bool) -> List[str]:
    #--- THIS METHOD SCRAPES THE PATHS TO EVERY WAVE FILE IN A GIVEN DIRECTORY
    paths = glob.glob(os.path.join(directory, '**', f'*.{file_ending}'), recursive=recursive)
    return paths

def map_vcm_to_full_terms(vcm: str) -> str:
    #--- THIS METHOD MAPS VCM SHORTCUTS TO FULL WORDS
    VCM_TO_FULL_TERMS = defaultdict(
        lambda: 'Unsure',
        {
            'N': 'Non-Canonical',
            'C': 'Canonical',
            'L': 'Laughing',
            'Y': 'Crying',
            'U': 'Unsure'
        },
    )
    return VCM_TO_FULL_TERMS[vcm]

def map_speaker_to_age(speaker: str) -> str:
    #--- THIS METHOD MAPS SPEAKER TO AGE
    SPEAKER_TO_AGE = defaultdict(
            lambda: 'U',
        {
            "CHI": "I",
            "CHI*": "I",
            "UI1": "I", # NOTE: the twin is counted as key-child!! change to "I" if the twin should be interpreted as other child
            "UI2": "I",
            "UI3": "I",
            "UI4": "I",
            "UI5": "I",
            "UI6": "I",
            "UI7": "I",
            "UI8": "I",
            "UI9": "I",
            "FA0": "A",
            "FA1": "A",
            "FA2": "A",
            "FA3": "A",
            "FA4": "A",
            "FA5": "A",
            "FA6": "A",
            "FA7": "A",
            "FA8": "A",
            "FA9": "A",
            "FC1": "C",
            "FC2": "C",
            "FC3": "C",
            "FC4": "C",
            "FC5": "C",
            "FC6": "C",
            "FC7": "C",
            "FC8": "C",
            "FC9": "C",
            "MA0": "A",
            "MA1": "A",
            "MA2": "A",
            "MA3": "A",
            "MA4": "A",
            "MA5": "A",
            "MA6": "A",
            "MA7": "A",
            "MA8": "A",
            "MA9": "A",
            "MC1": "C",
            "MC2": "C",
            "MC3": "C",
            "MC4": "C",
            "MC5": "C",
            "MC6": "C",
            "MC7": "C",
            "MC8": "C",
            "MC9": "C",
            "MI1": "I",
            "MOT*": "NA",
            "OC0": "C",
            "UC1": "C",
            "UC2": "C",
            "UC3": "C",
            "UC4": "C",
            "UC5": "C",
            "UC6": "C",
            "UC7": "C",
            "UC8": "C",
            "UC9": "C",
            "UA1": "A",
            "UA2": "A",
            "UA3": "A",
            "UA4": "A",
            "UA5": "A",
            "UA6": "A",
            "UA7": "A",
            "UA8": "A",
            "UA9": "A",
            "EE1": "NA",
            "EE2": "NA",
            "FAE": "A",
            "MAE": "A",
            "FCE": "C",
            "MCE": "C",
        },
    )
    return SPEAKER_TO_AGE[speaker]

def map_speaker_to_gender(speaker: str) -> str:
    #--- THIS METHOD MAPS SPEAKER TO GENDER
    SPEAKER_TO_GENDER = defaultdict(
            lambda: 'U',
        {
            "FA0": "F",
            "FA1": "F",
            "FA2": "F",
            "FA3": "F",
            "FA4": "F",
            "FA5": "F",
            "FA6": "F",
            "FA7": "F",
            "FA8": "F",
            "FA9": "F",
            "FC1": "F",
            "FC2": "F",
            "FC3": "F",
            "FC4": "F",
            "FC5": "F",
            "FC6": "F",
            "FC7": "F",
            "FC8": "F",
            "FC9": "F",
            "MA0": "M",
            "MA1": "M",
            "MA2": "M",
            "MA3": "M",
            "MA4": "M",
            "MA5": "M",
            "MA6": "M",
            "MA7": "M",
            "MA8": "M",
            "MA9": "M",
            "MC1": "M",
            "MC2": "M",
            "MC3": "M",
            "MC4": "M",
            "MC5": "M",
            "MC6": "M",
            "MC7": "M",
            "MC8": "M",
            "MC9": "M",
            "MI1": "M",
            "MOT*": "F",
            "FAE": "F",
            "MAE": "M",
            "FCE": "F",
            "MCE": "M",
        },
    )
    return SPEAKER_TO_GENDER[speaker]
    

def map_speaker_to_group(speaker: str) -> str:
    #--- THIS METHOD MAPS TWINS SPEAKERS TO VTC SPEAKER GROUPS
    SPEAKER_ID_TO_TYPE = defaultdict(
        lambda: "NA",
        {
            "CHI": "KCHI",
            "CHI*": "KCHI",
            "UI1": "OCH", # NOTE: the twin is counted as key-child!! change to "OCH" if the twin should be interpreted as other child
            "UI2": "OCH",
            "UI3": "OCH",
            "UI4": "OCH",
            "UI5": "OCH",
            "UI6": "OCH",
            "UI7": "OCH",
            "UI8": "OCH",
            "UI9": "OCH",
            "FA0": "FEM",
            "FA1": "FEM",
            "FA2": "FEM",
            "FA3": "FEM",
            "FA4": "FEM",
            "FA5": "FEM",
            "FA6": "FEM",
            "FA7": "FEM",
            "FA8": "FEM",
            "FA9": "FEM",
            "FC1": "OCH",
            "FC2": "OCH",
            "FC3": "OCH",
            "FC4": "OCH",
            "FC5": "OCH",
            "FC6": "OCH",
            "FC7": "OCH",
            "FC8": "OCH",
            "FC9": "OCH",
            "MA0": "MAL",
            "MA1": "MAL",
            "MA2": "MAL",
            "MA3": "MAL",
            "MA4": "MAL",
            "MA5": "MAL",
            "MA6": "MAL",
            "MA7": "MAL",
            "MA8": "MAL",
            "MA9": "MAL",
            "MC1": "OCH",
            "MC2": "OCH",
            "MC3": "OCH",
            "MC4": "OCH",
            "MC5": "OCH",
            "MC6": "OCH",
            "MC7": "OCH",
            "MC8": "OCH",
            "MC9": "OCH",
            "MI1": "OCH",
            "MOT*": "MAL",
            "OC0": "OCH",
            "UC1": "OCH",
            "UC2": "OCH",
            "UC3": "OCH",
            "UC4": "OCH",
            "UC5": "OCH",
            "UC6": "OCH",
            "UC7": "OCH",
            "UC8": "OCH",
            "UC9": "OCH",
            "UA1": "FEM", #UA
            "UA2": "FEM",
            "UA3": "FEM",
            "UA4": "FEM",
            "UA5": "FEM",
            "UA6": "FEM",
            "UA7": "FEM",
            "UA8": "FEM",
            "UA9": "FEM",
            "EE1": "NA",
            "EE2": "NA",
            "FAE": "FEM",
            "MAE": "MAL",
            "FCE": "OCH",
            "MCE": "OCH",
        },
    )
    return SPEAKER_ID_TO_TYPE[speaker]

#AUSDIEMAUS