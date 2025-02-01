from matplotlib import pyplot
import pybaseball as pb
import pandas
import argparse
from dataclasses import dataclass
import util
import pathlib
from typing import List

@dataclass
class Arguments:
    input: pathlib.Path
    output: pathlib.Path


def parse_args() -> Arguments:
    parser = argparse.ArgumentParser(
        description="Script to grab a baseball season and output CSV summary of hitters"
    )
    parser.add_argument("input", help="The file to use as input", type=pathlib.Path)
    parser.add_argument("output", help="The file to use as output", type=pathlib.Path)
    args = parser.parse_args()

    return Arguments(input=args.input, output=args.output)

@dataclass 
class Player:
    id: int 
    name: str 

    plate_appearences: int
    batted_balls: int

    average: float 
    obp: float 
    slg: float 
    ops: float 

    exit_velo_10th: float 
    exit_velo_avg: float
    exit_velo_90th: float 
    exit_velo_max: float 

    zcon: float 
    zcon_0_or_1_strikes: float
    zcon_2_strikes: float

if __name__ == "__main__":
    args = parse_args()

    year = pandas.read_csv(args.input)
    year = year[year["game_type"] == "R"]

    # output = open(args.output, mode="w")

    batter_ids = util.batter_ids(year)

    print(f"Gathering batting data for {len(batter_ids)} batters")

    players: List[Player] = []

    for id in batter_ids:
        
        name = pb.playerid_reverse_lookup([id], key_type="mlbam").iloc[0]
        pitches = year[year["batter"] == id]
        events = pitches[pitches['events'].notnull()]
        batted_balls = events[events['launch_speed'].notnull()]

        average = util.average(pitches)
        obp = util.obp(pitches)
        slg = util.slg(pitches)
        ops = obp + slg

        evs = util.evs(pitches).sort_values()
        if len(evs) == 0:
            continue 
        exit_velo_10th = evs.array[int(len(evs) * 0.1)]
        exit_velo_avg = evs.mean()
        exit_velo_90th = evs.array[int(len(evs) * 0.9)]
        exit_velo_max = evs.array[-1]
        
        two_strikes = pitches[pitches["strikes"] == 2]
        not_two_strikes = pitches[pitches["strikes"] < 2]
        
        zcon = util.zcon(pitches)
        zcon_0_or_1_strikes = util.zcon(not_two_strikes)
        zcon_2_strikes = util.zcon(two_strikes)
        
        summary = Player(
            id=id, 
            name=name['name_first'] + " " + name['name_last'],
            plate_appearences=len(events),
            batted_balls=len(batted_balls),
            average=average,
            obp=obp,
            slg=slg,
            ops=ops,
            exit_velo_10th=exit_velo_10th,
            exit_velo_avg=exit_velo_avg,
            exit_velo_90th=exit_velo_90th,
            exit_velo_max=exit_velo_max,
            zcon=zcon,
            zcon_0_or_1_strikes=zcon_0_or_1_strikes,
            zcon_2_strikes=zcon_2_strikes)
        players.append(summary)
    
    pandas.DataFrame(players).to_csv(args.output)