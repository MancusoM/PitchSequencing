# ======================================================
# Import Required Libraries
# ======================================================
# pandas → data manipulation
# Counter → count combinations easily

import pandas as pd
from collections import Counter
from typing import Union
from const import pitch_groups, pitch_types
from datetime import datetime
from pybaseball import statcast_pitcher
import polars as pl

# ======================================================
#  1️⃣  Retrieve MLBAM Id From Baseball Savant
# ======================================================


def retrieve_mlb_id(player_name: str, df: pd.DataFrame) -> Union[str, str]:
    """
    - Retrieves player MLBam ID using user-selected player name

    :param player_name:
    param df: players.csv
    :return: corresponding MLB AM ID
    """
    mlb_id = df.filter(pl.col("Name") == player_name)['MLBAMID'][0]
    team = df.filter(pl.col("Name") == player_name)['Team'][0]

    return mlb_id, team


# ======================================================
# 2️⃣  Retrieve Pitch-Level Data from Baseball Savant
# ======================================================
def call_statcast_pitcher(
    start_date: datetime.date, end_date: datetime.date, player_id: int, platoon: str
) -> pd.DataFrame:
    """

    :param start_date:
    :param end_date:
    :param player_id:
    :param platoon:
    :return:
    """
    df = pl.from_pandas(statcast_pitcher(str(start_date), str(end_date), player_id=player_id),schema_overrides= {"zone":pl.Int32,"batter":pl.Int32,'inning':pl.Int32,"outs":pl.Int32}).with_columns(pl.col('pitch_type')) #.fill_null(value = None).drop_nulls())

    # Preprocessing

    df = df.with_columns(
        pl.col("pitch_type")
        .map_elements(lambda x: pitch_types.get(x), return_dtype=pl.self_dtype())
        .alias("pitch_type"),
    )

    df = df.with_columns(
        pl.col("pitch_type")
        .map_elements(lambda x: pitch_groups.get(x), return_dtype=pl.self_dtype())
        .alias("pitch_group"),
    )

    if platoon == "LHB":
        return df.filter(pl.col("stand") > "L")
    elif platoon == "RHB":
        return df.filter(pl.col("stand") > "R")
    return df



# ======================================================
# 3️⃣Data Preprocessing
# ======================================================
def define_additional_cols(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """

    df = df.sort(
        ["game_date", "pitcher", "batter", "inning", "pitch_number"]
    )


    df = df.with_columns(
        new_ab=(pl.col("batter") != pl.col("batter").shift(1))
        |(pl.col("inning") != pl.col("inning").shift(1))
        | (pl.col("outs_when_up") < pl.col("outs_when_up").shift(1))
    .alias("new_ab").cast(pl.Int32))

    # Running total of new at-bats per pitcher = unique at-bat ID
    #df["at_bat_id"] = df.group_by("pitcher")["new_ab"].cumsum()
    df = df.with_columns(
        pl.col("new_ab").cum_sum().over("pitcher").alias("at_bat_id")
    )

    df = df.with_columns(
        pl.concat_str(["pitch_type", "zone"], separator="; Zone:").alias("pitch_zone_combo")
    )

    df = df.with_columns(
        pl.concat_str(["pitch_group", "zone"], separator="; Zone:").alias("pitch_group_combo")
    )

    return df

# ======================================================
# 4️⃣  Create a Sequence of Pitches for Each At-Bat
# ======================================================
# We now group the data by pitcher and at-bat, and collect the ordered list of pitches.
def create_pitch_sequencing(df: pd.DataFrame, choice: str) -> pd.DataFrame:
    """

    :param df:
    :param choice:
    :return:
    """

    return df.group_by(["pitcher", "at_bat_id"]).agg(pl.col(choice).alias("pitch_sequence"))


# ======================================================
# 5️⃣Extract and Count Pitch Combinations
# ======================================================
# We'll define a helper function that extracts consecutive pairs of pitches (2-pitch combos)
# Example: ['Fastball', 'Curveball', 'Slider'] → [('Fastball','Curveball'), ('Curveball','Slider')]


def get_combinations(seq: str, r=2) -> list:
    """Return all ordered combinations of length r (like pairs) from a sequence."""
    return [tuple(seq[i : i + r]) for i in range(len(seq) - r + 1)]


def count_combinations(pitch_sequences: pd.DataFrame):
    combo_counter = Counter()

    # Count combos for each pitcher across all at-bats
    for row in pitch_sequences.iter_rows():
        pitcher = row[0]
        seq = row[2]
        combos = get_combinations(seq, r=2)
        for c in combos:
            combo_counter[(pitcher, c)] += 1

    # Convert counts to DataFrame for easy filtering and visualization
    return pl.DataFrame(
        [(p, c[0], c[1], count) for (p, c), count in combo_counter.items()],
        schema = ["Pitcher", "Pitch 1", "Pitch 2", "Amount"],
    ).sort(["Pitcher", "Amount"], descending=[False, True])[
        [ "Pitch 1", "Pitch 2", "Amount"]
    ]


# To-Do
# Turn into Streamlit dashboard
# Add Player drop down to streamlit
# Add Savant Filtering
# Add 2/3 pitch filtering
# Add Team Filtering
# Add Export Button to different steps
# Split Files
# Add Platoon
# ways to export the data
# change everything to polars
