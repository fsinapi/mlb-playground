# MLB Statcast Data Playground

Repository to act as a playground for grabbing & playing with MLB batted ball data

## Setup

It is recommended to use this repository with a Python virtual environment. `scripts/init.sh` will set up a virtual environment `.venv` with the pybaseball package & some other tools for workign with the data.

## Get a season 

The script `src/get_season.py` will grab an entire season's worth of pitches and store it as a CSV. The data will be available at `data/{season}.csv`