# ======================================================
# 1️⃣  Import Required Libraries
# ======================================================
# pandas → data manipulation
# matplotlib → visualization
# Counter → count combinations easily

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import pybaseball as pyb

from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup

# Make plots look clean
sns.set(style="whitegrid", palette="deep", font_scale=1.1)
plt.rcParams["figure.figsize"] = (10, 5)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# ======================================================
# 1⃣  Retrieve Pitch-Level Data from Baseball Savant
# ======================================================

df = statcast_pitcher('2025-04-01', '2025-09-30', player_id = 519242)

df['zone'] = df['zone'].astype(int)
nulls = df.isna().sum()
print(f"Nulls Removed:{nulls}")
#df.dropna(inplace=True)

# Let's look at the first few rows to confirm structure

# We expect columns like:
# 'game_date', 'pitcher_name', 'batter_name', 'pitch_type', 'pitch_number', 'inning', 'outs'

# ======================================================
# 2️⃣  Load and Inspect Data
# ======================================================

# Replace with your actual file path
#df = pd.read_csv("holmes.csv")
# Let's look at the first few rows to confirm structure

# We expect columns like:
# 'game_date', 'pitcher_name', 'batter_name', 'pitch_type', 'pitch_number', 'inning', 'outs'

# ======================================================
# 3️⃣  Sort Pitches in Correct Chronological Order
# ======================================================
# Sorting ensures pitches are processed in the real sequence they occurred.
# This matters because combinations depend on the order.

df = df.sort_values(
    ['game_date', 'pitcher', 'batter', 'inning', 'pitch_number']
).reset_index(drop=True)
# ======================================================
# 4️⃣  Automatically Detect At-Bats
# ======================================================
# An "at-bat" is the full sequence of pitches a single batter faces before
# the result (hit, out, walk, etc.)
#
# Many CSVs don't include explicit at-bat IDs, so we reconstruct them logically:
# A new at-bat starts when:
#   - A new batter comes up
#   - A new inning starts
#   - The outs reset (meaning the half-inning has changed)

df['new_ab'] = (
    (df['batter'] != df['batter'].shift(1)) |
    (df['inning'] != df['inning'].shift(1)) |
    (df['outs_when_up'] < df['outs_when_up'].shift(1))
).astype(int)

# Running total of new at-bats per pitcher = unique at-bat ID
df['at_bat_id'] = df.groupby('pitcher')['new_ab'].cumsum()

df['pitch_zone_combo'] = df.apply(lambda row: f"{row['pitch_type']}, {row['zone']}", axis=1)

#df['fixed'] = df['pitch_type_zone'].apply(lambda x: x.strip().replace('\n','').replace('        ',''))
# ======================================================
# 5️⃣  Create a Sequence of Pitches for Each At-Bat
# ======================================================
# We now group the data by pitcher and at-bat, and collect the ordered list of pitches.

pitch_sequences = (
    df.groupby(['pitcher', 'at_bat_id'])['pitch_zone_combo']
      .apply(list)
      .reset_index(name='pitch_sequence')
)

# Let's look at a few
print(pitch_sequences.head(20))

# Example:
# Pitcher 1, At-bat 1: ['Fastball', 'Curveball', 'Slider']
# Pitcher 1, At-bat 2: ['Fastball', 'Curveball', 'Curveball', 'Slider']


# ======================================================
# 6️⃣  Extract and Count Pitch Combinations
# ======================================================
# We'll define a helper function that extracts consecutive pairs of pitches (2-pitch combos)
# Example: ['Fastball', 'Curveball', 'Slider'] → [('Fastball','Curveball'), ('Curveball','Slider')]

def get_combinations(seq, r=2):
    """Return all ordered combinations of length r (like pairs) from a sequence."""
    return [tuple(seq[i:i+r]) for i in range(len(seq)-r+1)]

combo_counter = Counter()

# Count combos for each pitcher across all at-bats
for _, row in pitch_sequences.iterrows():
    pitcher = row['pitcher']
    seq = row['pitch_sequence']
    combos = get_combinations(seq, r=2)
    for c in combos:
        combo_counter[(pitcher, c)] += 1

# Convert counts to DataFrame for easy filtering and visualization
combo_df = (
    pd.DataFrame(
        [(p, c[0], c[1], count) for (p, c), count in combo_counter.items()],
        columns=['pitcher', 'pitch1', 'pitch2', 'count']
    )
    .sort_values(['pitcher', 'count'], ascending=[True, False])
)

filtered = combo_df[combo_df['count']>1]
print(filtered.head(20))

#To-Do
#Turn into Streamlit dashboard
# Add Player drop down to streamlit
# Add Savant Filtering
# Add 2/3 pitch filtering
# Add Team Filtering
# Add Export Button to different steps
# Split Files
