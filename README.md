# Pitch Sequencing 

This Python script powers the backend of a Streamlit "Pitch Sequencing" Dashboard that interacts with pybaseball to display real-time pitch sequencing data. This data is processed and returned as Polars DataFrames for easy manipulation and analysis.

- Python 3.x
- `polars` library
- `pandas` library
- `pybaseball` library
- `streamlit` library
- `pathlib` library
- `typing` library

## Folders 
#### `Calculations`

##### calculate_sequencing.py
Stores functions that ingest, massage, format, and normalize PyBaseball data to calculate pitch sequences

#### 'Data'
- Player data from Fangraphs. used to merge data from PyBaseball using the 'MLBAMID'

#### 'helper_functions'
- runs main functions, creates csv export functionality, returns streamlit table to website, calculates team and league percentages

#### 'website'
- set streamlit functionality

#### 'images'
- example conclusions generated from website
