# MLB Statcast Data Playground

Repository to act as a playground for grabbing & playing with MLB batted ball data

## Setup

It is recommended to use this repository with a Python virtual environment. `scripts/init.sh` will set up a virtual environment `.venv` with the pybaseball package & some other tools for workign with the data.

## Running Code

After creating the virtual environment, you can access it with the command:

```shell
$ source .venv/bin/activate
```

### Getting data

Most of the scripts rely on caching a season as a CSV in the `data/` folder. The script `get_season.py` will retrieve a season and save it to your local drive.

### Running Shiny apps

Some of the scripts are shiny apps (those beginning with `app_`). To run these, use the command:

```shell
$ shiny run --reload --launch-browser `path/to/script`
```

The app will be available in a browser window at `http://127.0.0.1:8000/`