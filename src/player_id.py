# Script to look up player ID's

import pybaseball as pb
import argparse
from dataclasses import dataclass


@dataclass
class Arguments:
    first: str
    last: str


def parse_args() -> Arguments:
    parser = argparse.ArgumentParser(description="Script to search for a Player ID")
    parser.add_argument("first", help="The player's first name", type=str)
    parser.add_argument("last", help="The player's last name", type=str)
    args = parser.parse_args()

    return Arguments(first=args.first, last=args.last)


if __name__ == "__main__":
    args = parse_args()

    print(f'Looking up "{args.first} {args.last}"')

    data = pb.playerid_lookup(last=args.last, first=args.first, fuzzy=True)
    if len(data) == 0:
        print(f'Could not find player "{args.first} {args.last}"')
        exit(1)

    print(f"Found {len(data)} players:")
    print(data)
