from matplotlib import pyplot
import pybaseball as pb
import argparse
from dataclasses import dataclass
import util


@dataclass
class Arguments:
    playerid: int
    year: int


def parse_args() -> Arguments:
    parser = argparse.ArgumentParser(
        description="Script to grab a baseball season and grab every pitch from the  year"
    )
    parser.add_argument("playerid", help="The player MLBAM id", type=int)
    parser.add_argument("year", help="The year to search", type=int)
    args = parser.parse_args()

    return Arguments(playerid=args.playerid, year=args.year)


if __name__ == "__main__":
    args = parse_args()

    data = pb.statcast_pitcher(
        start_dt=f"{args.year}-01-01",
        end_dt=f"{args.year}-12-31",
        player_id=args.playerid,
    )

    pitches = data[data["game_type"] == "R"]

    pitch_types = util.pitch_types(pitches)

    fig, ax = pyplot.subplots()
    for pitch in pitch_types:
        p = pitches[pitches["pitch_name"] == pitch]

        x = p["pfx_x"]
        y = p["pfx_z"]

        ax.scatter(x=x.values, y=y.values, label=pitch)

    ax.legend()
    ax.grid(True)

    # name = pb.playerid_reverse_lookup(player_ids=[args.playerid], key_type='mlbam').iloc[0]
    # pyplot.savefig(f'output/{name['name_first']}-{name['name_last']}-{name['key_mlbam']}.png')
    pyplot.show()
