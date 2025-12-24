# Pitch Sequencing 

This Python script powers the backend of a Streamlit "Pitch Sequencing" Dashboard that interacts with pybaseball to display real-time pitch sequencing data. This data is processed and returned as Polars DataFrames for easy manipulation and analysis.

- `Python` 3.x
- `polars` library
- `pandas` library
- `pybaseball` library
- `streamlit` library
- `pathlib` library
- `typing` library

## Folders 
#### Calculations

- calculate_sequencing.py
  - Stores functions that ingest, massage, format, and normalize PyBaseball data to calculate pitch sequences

#### Data
- players.csv
    - Player data used to merge data from PyBaseball using the 'MLBAMID'
- teams.csv
  - CSV that returns the data in the Team & League filter

#### helper_functions
- helpers.py
    - runs main functions, creates CSV export functionality, returns streamlit table to website, calculates team and league percentages

#### website_operations
- website.py
  - sets streamlit functionality, formats webpage
- website_funcs.py
    - runs the real-time calculations to return the player pitch sequence

#### images
- Conclusions generated from the `Pitch Sequencing` streamlit application
  - Example 1:
      - xyz
  - Example 2:
      - abc
