from pathlib import Path

# Retreats Directory From Parent Path
current_script_path = Path(__file__).resolve()
parent_directory = current_script_path.parent

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from calculations.calculate_sequencing import (
    retrieve_mlb_id,
    call_statcast_pitcher,
    define_additional_cols,
    create_pitch_sequencing,
    count_combinations,
)
from typing import Any
import polars as pl


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
        table that's generated in Streamlit
        pitch_sequences: returned to data can be downloaded

    """

    mlbID = retrieve_mlb_id(pitcher, players)

    player_pitch_data = call_statcast_pitcher(
        selected_range[0], selected_range[1], mlbID, platoon
    )

    enriched_player_data = define_additional_cols(player_pitch_data)
    pitch_sequences = create_pitch_sequencing(enriched_player_data, sequencing_choice)
    table = count_combinations(pitch_sequences).head(15)

    return table, pitch_sequences, mlbID


""""""
