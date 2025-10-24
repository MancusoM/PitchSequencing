# ======================================================
# 1️⃣  Import Required Libraries
# ======================================================
# pandas → data manipulation
# Counter → count combinations easily

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import pybaseball as pyb
import streamlit as st
from typing import Union

from pybaseball import statcast_pitcher
from datetime import date, datetime

# Make plots look clean
# sns.set(style="whitegrid", palette="deep", font_scale=1.1)
plt.rcParams["figure.figsize"] = (10, 5)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

###### returns the bref ids of David Peterson (returns one row)


def retrieve_mlb_id(player_name, df) -> Union[str, str]:
    """
    - Retrieves player MLBam ID using user-selected player name

    :param player_name:
    param df: players.csv
    :return: corresponding MLB AM ID
    """
    mlb_id, team = (
        df.loc[df["Name"] == player_name, "MLBAMID"].iloc[0],
        df.loc[df["Name"] == player_name, "Team"].iloc[0],
    )
    return mlb_id, team


# ======================================================
# 1⃣  Retrieve Pitch-Level Data from Baseball Savant
# ======================================================


def call_statcast_pitcher(start_date, end_date, player_id):
    """

    :param start_date:
    :param end_date:
    :param player_id:
    :return:
    """

    df = statcast_pitcher(str(start_date), str(end_date), player_id=player_id).dropna(
        subset=["pitch_type"]
    )
    # Preprocessing
    df["zone"] = df["zone"].astype(int)
    # Remove Nulls From DataFrame
    nulls = df.isna().sum()
    # st.write(f"Nulls Removed:{nulls}")
    return df


# ======================================================
# [2]Data Preprocessing
# ======================================================
def define_additional_cols(df):
    """

    :param df:
    :return:
    """

    df = df.sort_values(
        ["game_date", "pitcher", "batter", "inning", "pitch_number"]
    ).reset_index(drop=True)

    df["new_ab"] = (
        (df["batter"] != df["batter"].shift(1))
        | (df["inning"] != df["inning"].shift(1))
        | (df["outs_when_up"] < df["outs_when_up"].shift(1))
    ).astype(int)

    # Running total of new at-bats per pitcher = unique at-bat ID
    df["at_bat_id"] = df.groupby("pitcher")["new_ab"].cumsum()

    df["pitch_zone_combo"] = df.apply(
        lambda row: f"{row['pitch_type']}, {row['zone']}", axis=1
    )
    return df


# ======================================================
# 5️⃣  Create a Sequence of Pitches for Each At-Bat
# ======================================================
# We now group the data by pitcher and at-bat, and collect the ordered list of pitches.
def create_pitch_sequencing(df):
    """

    :param df:
    :return:
    """
    return (
        df.groupby(["pitcher", "at_bat_id"])["pitch_zone_combo"]
        .apply(list)
        .reset_index(name="pitch_sequence")
    )

# ======================================================
# 3️  Extract and Count Pitch Combinations
# ======================================================
# We'll define a helper function that extracts consecutive pairs of pitches (2-pitch combos)
# Example: ['Fastball', 'Curveball', 'Slider'] → [('Fastball','Curveball'), ('Curveball','Slider')]

def get_combinations(seq, r=2):
    """Return all ordered combinations of length r (like pairs) from a sequence."""
    return [tuple(seq[i : i + r]) for i in range(len(seq) - r + 1)]

def count_combinations(pitch_sequences):
    combo_counter = Counter()

    # Count combos for each pitcher across all at-bats
    for _, row in pitch_sequences.iterrows():
        pitcher = row["pitcher"]
        seq = row["pitch_sequence"]
        combos = get_combinations(seq, r=2)
        for c in combos:
            combo_counter[(pitcher, c)] += 1

    # Convert counts to DataFrame for easy filtering and visualization
    return pd.DataFrame(
        [(p, c[0], c[1], count) for (p, c), count in combo_counter.items()],
        columns=["pitcher", "pitch1", "pitch2", "count"],
    ).sort_values(["pitcher", "count"], ascending=[True, False])


# To-Do
# Turn into Streamlit dashboard
# Add Player drop down to streamlit
# Add Savant Filtering
# Add 2/3 pitch filtering
# Add Team Filtering
# Add Export Button to different steps
# Split Files
# Add Platoon
#ways to export the data