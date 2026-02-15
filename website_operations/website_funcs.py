import sys
import os

from typing import Any
from pathlib import Path
import polars as pl
import streamlit as st

from calculations.calculate_sequencing import (
    retrieve_mlb_id,
    call_statcast_pitcher,
    define_additional_cols,
    create_pitch_sequencing,
    count_combinations,
)

# Retrieves Directory From Parent Path
current_script_path = Path(__file__).resolve()
parent_directory = current_script_path.parent

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

st.cache_data()


def calculate_sequence(
    pitcher: str,
    players: pl.DataFrame,
    sequencing_choice: str,
    selected_range: Any,
    platoon: str,
):
    """

    Runs the five core functions that creates the sequencing dashboard

    :param pitcher: Pitcher selected in streamlit drop-down
    :param players: players.csv df
    :param sequencing_choice: choice of pitch type w or w/o location & pitch group w or w/o location
    :param selected_range: select range from Streamlit Calendar
    :param platoon: applicable if the user selects a filter option on Streamlit

    :return:
        table: formatted pitch sequencing table that's generated in Streamlit
        pitch_sequences: untransformed sequencing data can be downloaded

    """

    mlbID = retrieve_mlb_id(pitcher, players)

    player_pitch_data = call_statcast_pitcher(
        selected_range[0], selected_range[1], mlbID, platoon
    )

    enriched_player_data = define_additional_cols(player_pitch_data)
    pitch_sequences = create_pitch_sequencing(enriched_player_data, sequencing_choice)
    table = count_combinations(pitch_sequences).head(20)
    return table, pitch_sequences, mlbID
