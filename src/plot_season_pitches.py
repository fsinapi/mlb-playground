from matplotlib import pyplot
import pybaseball as pb
import pandas
import argparse
from dataclasses import dataclass
import util


@dataclass
class Arguments:
    file: str


def parse_args() -> Arguments:
    parser = argparse.ArgumentParser(
        description="Script to grab a baseball season and plot pitch arsenals for every player that year"
    )
    parser.add_argument("file", help="The file to use as input", type=str)
    args = parser.parse_args()

    return Arguments(file=args.file)


if __name__ == "__main__":
    args = parse_args()

    year = pandas.read_csv(args.file)
    year = year[year["game_type"] == "R"]

    pitcher_ids = util.pitcher_ids(year)

    index = open("output/index.html", mode="w")

    print(f"Plotting data for {len(pitcher_ids)} pitchers")

    for id in pitcher_ids:

        pitches = year[year["pitcher"] == id]
        pitch_types = util.pitch_types(pitches)

        fig, ax = pyplot.subplots()
        for pitch in pitch_types:
            p = pitches[pitches["pitch_name"] == pitch]

            x = p["pfx_x"]
            y = p["pfx_z"]

            ax.scatter(x=x.values, y=y.values, label=pitch)

        ax.legend()
        ax.grid(True)

        name = pb.playerid_reverse_lookup(player_ids=[id], key_type="mlbam").iloc[0]
        filename = f"{name['name_first']}-{name['name_last']}-{name['key_mlbam']}"
        pyplot.savefig(f"output/{filename}.png")
        pyplot.close(fig=fig)
        index.write(f"<a href={filename}.png>{filename}</a>\n")
