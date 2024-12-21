# Script to grab a season and save it as a CSV

import pybaseball as pb 
import argparse 
from dataclasses import dataclass

@dataclass
class Arguments:
    year: int

def parse_args() -> Arguments:
    parser = argparse.ArgumentParser(description='Script to grab a baseball season and grab every pitch from the  year')
    parser.add_argument('year', help='The year to grab data from', type=int)
    args = parser.parse_args()

    return Arguments(year=args.year)

if __name__ == '__main__':
    args = parse_args()

    data = pb.statcast(start_dt=f'{args.year}-01-01', end_dt=f'{args.year}-12-01')
    data.to_csv(f'data/{args.year}.csv')