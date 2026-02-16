# ======================================================
# Import Required Libraries
# ======================================================

from collections import Counter
from const import pitch_types
from datetime import datetime
from pybaseball import statcast_pitcher
import polars as pl
import streamlit as st

# ======================================================
#  1️⃣  Retrieve MLBAM Id From Baseball Savant
# ======================================================


def retrieve_mlb_id(player_name: str, players_df: pl.DataFrame) -> int:
    """
    - Retrieves player MLBAM ID from user-selected player name

    :param player_name: Player Name chosen from Streamlit drop-down
    :param players_df: players.csv
    :return: corresponding MLBAM ID
    """

    return players_df.filter(pl.col("Name") == player_name)["MLBAMID"][0]


# ======================================================
# 2️⃣  Retrieve Pitch-Level Data from Baseball Savant
# ======================================================
def call_statcast_pitcher(
    start_date: datetime.date, end_date: datetime.date, player_id: int, platoon: str
) -> pl.DataFrame:
    """

    Calls pybaseball's statcast_pitcher module and converts it into polars for faster processing

    docs: https://github.com/jldbc/pybaseball/blob/master/docs/statcast_pitcher.md

    :param start_date: start date of query
    :param end_date: end date of query
    :param player_id: MLB AM id necessary to scrape Savant data
    :param platoon: applicable if the user selects a filter option on Streamlit
    :return: a filtered scrape from Baseball Savant
    """
    try:
        df = pl.from_pandas(
            statcast_pitcher(str(start_date), str(end_date), player_id=player_id),
            schema_overrides={
                "zone": pl.Int32,
                "batter": pl.Int32,
                "inning": pl.Int32,
                "outs": pl.Int32,
            },
        )
    except Exception as e:
        st.error("Statcast API failed. Error: ", e, icon="⚠️")

    # Preprocessing

    df = df.with_columns(
        pl.col("pitch_type")
        .map_elements(lambda x: pitch_types.get(x), return_dtype=pl.self_dtype())
        .alias("pitch_type"),
    )

    if platoon == "LHB":
        return df.filter(pl.col("stand") == "L")
    elif platoon == "RHB":
        return df.filter(pl.col("stand") == "R")
    return df.drop_nulls(subset=["pitch_type"])


# ======================================================
# 3️⃣Data Preprocessing
# ======================================================
def define_additional_cols(uneriched_data: pl.DataFrame) -> pl.DataFrame:
    """

    Data Transformation:
        - Sorts
        - Creates New Col to account for new AB
            - Running total of new at-bats per pitcher = unique at-bat ID
            - df["at_bat_id"] = df.group_by("pitcher")["new_ab"].cumsum()
        - Manually adds columns to be filtered on in Streamlit

    :param uneriched_data unenriched data from Savant Scrape
    :return: enriched data with all necessary columns for sequencing calculations
    """

    return (
        uneriched_data.sort(
            ["game_date", "pitcher", "batter", "inning", "pitch_number"]
        )
        .with_columns(
            new_ab=(pl.col("batter") != pl.col("batter").shift(1))
            | (pl.col("inning") != pl.col("inning").shift(1))
            | (pl.col("outs_when_up") < pl.col("outs_when_up").shift(1))
            .alias("new_ab")
            .cast(pl.Int32)
        )
        .with_columns(pl.col("new_ab").cum_sum().over("pitcher").alias("at_bat_id"))
        .with_columns(
            pl.concat_str(["pitch_type", "zone"], separator="; Zone:").alias(
                "pitch_zone_combo"
            )
        )
    )


# ======================================================
# 4️⃣  Create a Sequence of Pitches for Each At-Bat
# ======================================================


# We now group the data by pitcher and at-bat, and collect the ordered list of pitches.
def create_pitch_sequencing(enriched_df: pl.DataFrame, choice: str) -> pl.DataFrame:
    """

    :param enriched_df: enriched_data from the 'define_addtional_cols' function
    :param choice: choice of pitch type w or w/o location
    :return: pitch that grouped by pitcher and unique at-bat
    """

    return enriched_df.group_by(["pitcher", "at_bat_id"]).agg(
        pl.col(choice).alias("pitch_sequence")
    )


# ======================================================
# 5️⃣Extract and Count Pitch Combinations
# ======================================================
# We'll define a helper function that extracts consecutive pairs of pitches (2-pitch combos)
# Example: ['Fastball', 'Curveball', 'Slider'] → [('Fastball','Curveball'), ('Curveball','Slider')]


def get_combinations(seq: str, r=2) -> list:
    """Return all ordered combinations of length r (like pairs) from a sequence.

    :param: seq: sequence of pitches
    :param r : the length of each sequence (default = 2)
    returns ordered combinations of paired pitches
    """

    return [tuple(seq[i : i + r]) for i in range(len(seq) - r + 1)]


def count_combinations(pitch_sequences: pl.DataFrame) -> pl.DataFrame:
    """
    Count of combinations from each pitch sequence list

    :param pitch_sequences: grouped data from the 'create_pitch_sequencing'
    :return: DataFrame with each pitcher's most frequent pair

    """

    combo_counter = Counter()

    # Count combos for each pitcher across all at-bats
    for row in pitch_sequences.iter_rows():
        pitcher = row[0]
        seq = row[2]
        combos = get_combinations(seq, r=2)
        for c in combos:
            combo_counter[(pitcher, c)] += 1

    # Convert counts to DataFrame for easy filtering and visualization
    return (
        pl.DataFrame(
            [(p, c[0], c[1], count) for (p, c), count in combo_counter.items()],
            schema=["Pitcher", "Pitch 1", "Pitch 2", "Amount"],
            orient="row",
        )
        .sort(["Pitcher", "Amount"], descending=[False, True])
        .with_columns(
            pl.col("Amount").truediv((pl.col("Amount").sum()) / 100).round(2).alias("%")
        )
    )
