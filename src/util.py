"""Utilities for working with statcast data."""

import pybaseball as pb
from pandas import DataFrame

swinging_descriptions = [
    "hit_into_play",
    "foul",
    "swinging_strike",
    "swinging_strike_blocked",
    "foul_tip",
]

contact_descriptions = [
    "hit_into_play",
    "foul",
]


def zcon(data: DataFrame) -> float:
    """
    Calculate ZCon% for a dataset of pitches. They should already be filtered to whatever
    player(s) you want to analyze."""

    d2 = data[data["zone"] <= 9]
    zone_swings = d2[d2["description"].isin(swinging_descriptions)]
    # [data['description'] in swinging_descriptions]
    zone_contact = zone_swings[zone_swings["description"].isin(contact_descriptions)]
    return float(len(zone_contact)) / float(len(zone_swings))


# List of event strings that Statcast uses
all_events = [
    "strikeout",
    "field_out",
    "walk",
    "single",
    "double",
    "sac_fly",
    "catcher_interf",
    "force_out",
    "hit_by_pitch",
    "fielders_choice",
    "field_error",
    "home_run",
    "grounded_into_double_play",
    "double_play",
    "strikeout_double_play",
    "fielders_choice_out",
    "truncated_pa",
    "sac_bunt",
    "triple",
    "triple_play",
    "sac_fly_double_play",
]

hit_events = [
    "single",
    "double",
    "home_run",
    "triple",
    "triple_play",
]

nonhit_avg_events = [
    "strikeout",
    "field_out",
    "force_out",
    "fielders_choice",
    "field_error",
    "grounded_into_double_play",
    "double_play",
    "strikeout_double_play",
    "fielders_choice_out",
    "triple_play",
]

def average(data: DataFrame) -> float:
    """
    Calculate batting average for a dataset of pitches.
    They should already be filtered to whatever player(s) you want to analyze.
    """

    hits = data[data['events'].isin(hit_events)]
    nonhit_nonwalk = data[data['events'].isin(nonhit_avg_events)]
    return len(hits) / (len(hits) + len(nonhit_nonwalk))