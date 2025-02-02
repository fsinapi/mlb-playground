from matplotlib import pyplot
import pybaseball as pb
import pandas
import argparse
from dataclasses import dataclass
import util
from shiny.express import input, render, ui
from typing import List
import numpy as np
import os
import requests
import tempfile

year = pandas.read_csv("data/2024.csv")
year = year[year["game_type"] == "R"]

pitcher_ids = util.pitcher_ids(year)

names = pb.playerid_reverse_lookup(player_ids=pitcher_ids, key_type="mlbam")

name_choices = {
    n["key_mlbam"]: n["name_first"] + " " + n["name_last"] for _, n in names.iterrows()
}

ui.input_select(
    id="pitcher_id",
    label="Select pitcher to plot",
    choices=name_choices,
)

with ui.card():
    ui.card_header("Summary")

    @render.text()
    def name():
        id = input.pitcher_id()
        name = pb.playerid_reverse_lookup(player_ids=[int(id)], key_type="mlbam").iloc[
            0
        ]
        return f"{name["name_first"]} {name["name_last"]} [{id}]"

    with ui.layout_columns(col_widths=[5, 7], fill=True):

        @render.image(delete_file=True)
        def picture():
            id = str(input.pitcher_id())
            filepath = ""
            url = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:silo:current.png/r_max/w_180,q_auto:best/v1/people/{id}/headshot/silo/current"
            with tempfile.NamedTemporaryFile(delete=False) as pic:
                filepath = pic.name
                pic.write(requests.get(url).content)
            return {
                "src": filepath,
                "width": "180px",
                "height": "180px",
            }

        @render.table(index=True)
        def results_summary():
            id = input.pitcher_id()
            pitches = year[year["pitcher"] == np.int64(id)]
            sum = pitches.sum(axis=0, numeric_only=True)
            return pandas.DataFrame(
                data=[len(pitches), sum.loc["post_bat_score"] - sum.loc["bat_score"]],
                index=["Pitches Thrown", "Runs Allowed"],
            )


with ui.card():
    ui.card_header("Pitch Arsenal")

    @render.plot
    def arsenal():
        id = input.pitcher_id()
        pitches = year[year["pitcher"] == np.int64(id)]
        pitch_types = util.pitch_types(pitches)
        fig, ax = pyplot.subplots()
        for pitch in pitch_types:
            p = pitches[pitches["pitch_name"] == pitch]

            x = p["pfx_x"]
            y = p["pfx_z"]

            ax.scatter(x=x.values, y=y.values, label=pitch)
        pyplot.xlabel("Horizontal Induced Break (ft)")
        pyplot.ylabel("Vertical Induced Break (ft)")
        ax.legend()
        ax.grid(True)
        return fig

    @render.data_frame
    def pitch_info():
        id = input.pitcher_id()
        pitches = year[year["pitcher"] == np.int64(id)]
        pitch_types = util.pitch_types(pitches)
        columns = [
            "pitch type",
            "average velo",
            "velo stdev",
            "average arm angle",
            "arm angle stdev",
            "average horizontal break",
            "horizontal break stdev",
            "average vertical break",
            "vertical break stdev",
        ]
        data = []
        for pitch in pitch_types:
            p: pandas.DataFrame = pitches[pitches["pitch_name"] == pitch]

            means = p.mean(axis=0, numeric_only=True)
            stdevs = p.std(axis=0, numeric_only=True)

            data.append(
                (
                    str(pitch),
                    means.loc["release_speed"],
                    stdevs.loc["release_speed"],
                    means.loc["arm_angle"],
                    stdevs.loc["arm_angle"],
                    means.loc["pfx_x"],
                    stdevs.loc["pfx_x"],
                    means.loc["pfx_z"],
                    stdevs.loc["pfx_z"],
                )
            )
        return pandas.DataFrame(data=data, columns=columns)
