from pybaseball import statcast
from calculations.calculate_sequencing import (
    define_additional_cols,
    create_pitch_sequencing,
    count_combinations,
)
import polars as pl
from const import pitch_groups, pitch_types, team_list, mlb_2025_dates
import time
from datetime import datetime
from helper_functions.helpers import calculate_percentage, read_df

from pathlib import Path

current_script_path = Path(__file__).resolve()
parent_directory = current_script_path.parent.parent

# Get the current datetime object
now = datetime.now()

# Format the datetime object into a readable string
pretty_time = now.strftime("%B %d, %Y at %I:%M %p")
print(pretty_time)
players = read_df(parent_directory / "data/players.csv")  # type:ignore


for team in team_list[18:19]:  # 18:21
    teams_df = pl.DataFrame()
    print("Processing:", team)

    opening, closing = mlb_2025_dates.get(team)[0], mlb_2025_dates.get(team)[1]

    try:
        data = (
            pl.from_pandas(
                statcast(opening, closing, team)[
                    [
                        "player_name",
                        "game_date",
                        "outs_when_up",
                        "batter",
                        "inning",
                        "pitch_number",
                        "pitcher",
                        "stand",
                        "pitch_type",
                        "zone",
                    ]
                ],
                schema_overrides={
                    "zone": pl.Int32,
                    "batter": pl.Int32,
                    "inning": pl.Int32,
                    "outs": pl.Int32,
                },
            )
            .drop_nulls(subset=["pitch_type", "zone"])
            .with_columns(
                pl.col("pitch_type")
                .map_elements(
                    lambda x: pitch_types.get(x), return_dtype=pl.self_dtype()
                )
                .alias("pitch_type"),
            )
            .with_columns(
                pl.col("pitch_type")
                .map_elements(
                    lambda x: pitch_groups.get(x), return_dtype=pl.self_dtype()
                )
                .alias("pitch_group"),
            )
        )

    except:
        raise ConnectionError("API timed out or return consists of an empty DataFrame")

    enriched_data = define_additional_cols(data)
    dataframe = pl.DataFrame()
    for i in ["pitch_type", "pitch_zone_combo", "pitch_group", "pitch_group_combo"]:
        pitch_sequences = create_pitch_sequencing(enriched_data, i)
        combinations = count_combinations(pitch_sequences)
        team_combinations = (
            combinations.join(
                players, how="left", left_on="Pitcher", right_on="MLBAMID"
            )[["Pitcher", "Name", "Pitch 1", "Pitch 2", "Amount"]]
            .with_columns(pl.lit(team).alias("Team"))
            .with_columns(pl.lit(i).alias("Call"))
        )

        percentages = calculate_percentage(team_combinations)

        enriched_team_combinations = percentages.with_columns(
            ((pl.col("Amount") / pl.col("Amount_right") * 100).round(2)).alias("%")
        )
        dataframe = pl.concat([dataframe, enriched_team_combinations])

    dataframe.to_pandas().to_csv(
        f"{parent_directory}/data/teams.csv", mode="a", index=False, header=False
    )

    now = datetime.now()

    # Format the datetime object into a readable string
    # Example format: "October 30, 2025 at 08:13 PM"
    pretty_time = now.strftime("%B %d, %Y at %I:%M %p %S")
    print(f"Going to sleep now at {pretty_time}")
    time.sleep(40)

now = datetime.now()

# Format the datetime object into a readable string
# Example format: "October 30, 2025 at 08:13 PM"
pretty_time = now.strftime("%B %d, %Y at %I:%M:%p")

print(pretty_time)
