# Script to grab a player's statcast and calculate some stuff

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
    parser.add_argument("--type", help="The year to search", type=int)
    args = parser.parse_args()

    return Arguments(playerid=args.playerid, year=args.year)


if __name__ == "__main__":
    args = parse_args()

    data = pb.statcast_batter(
        start_dt=f"{args.year}-01-01",
        end_dt=f"{args.year}-12-31",
        player_id=args.playerid,
    )
    # data.to_csv(f'data/{args.playerid}-{args.year}.csv')
    regular = data[data["game_type"] == "R"]

    avg = util.average(regular)

    two_strikes = regular[regular["strikes"] == 2]
    not_two_strikes = regular[regular["strikes"] < 2]

    evs = util.evs(regular)

    evs = evs.sort_values()
    ev_10th = evs.array[int(len(evs) * 0.1)]
    ev_90th = evs.array[int(len(evs) * 0.9)]
    ev_max = evs.array[-1]

    zcon = util.zcon(regular)
    zcon_01 = util.zcon(not_two_strikes)
    zcon_2 = util.zcon(two_strikes)
    print(f"Average:                  {avg}")
    print("")
    print(f"Overall zone contact:     {zcon * 100}")
    print(f"ZCon% with 0 or 1 strike: {zcon_01 * 100}")
    print(f"ZCon% with 2 strikes:     {zcon_2 * 100}")
    print(f"10% Exit Velo:            {ev_10th}")
    print(f"90% Exit Velo:            {ev_90th}")
    print(f"Max Exit Velo:            {ev_max}")
