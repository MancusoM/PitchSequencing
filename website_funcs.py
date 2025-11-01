from typing import AnyStr

import streamlit as st

from sequencingCalc import (
    retrieve_mlb_id,
    call_statcast_pitcher,
    define_additional_cols,
    create_pitch_sequencing,
    count_combinations,
)
from uuid import uuid4
import pandas as pd
from typing import Any


def main(
    pitcher: str,
    players: pd.DataFrame,
    sequencing_choice: str,
    selected_range: Any,
    platoon: str,
):
    """


    :param pitcher:
    :param players:
    :param choice:
    :param selected_range:
    :param platoon:
    :return:
    """

    mlbID, team = retrieve_mlb_id(pitcher, players)

    player_pitch_data = call_statcast_pitcher(
        selected_range[0], selected_range[1], mlbID, platoon
    )

    enriched_player_data = define_additional_cols(player_pitch_data)
    pitch_sequences = create_pitch_sequencing(enriched_player_data, sequencing_choice)
    table = count_combinations(pitch_sequences).head(15)

    return table, pitch_sequences


def create_csv_button(df, name):
    st.download_button(
        f"Download {name}",
        df.to_csv(index=False).encode("utf-8"),
        f"{name}.csv",
        "text/csv",
        key=uuid4(),
    )
