"""Utilities for working with statcast data."""

import pybaseball as pb
from pandas import DataFrame, Series
import numpy

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
    if len(zone_swings) == 0:
        return 0
    return float(len(zone_contact)) / float(len(zone_swings))


# List of event strings that Statcast uses
all_events = [
    "strikeout",
    "field_out",
    "walk",
    "single",
    "double",
    "intent_walk",
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
    hits = data[data["events"].isin(hit_events)]
    nonhit_nonwalk = data[data["events"].isin(nonhit_avg_events)]
    return len(hits) / (len(hits) + len(nonhit_nonwalk))


on_base_events = [
    "walk",
    "single",
    "double",
    "hit_by_pitch",
    "home_run",
    "triple",
    "intent_walk",
]

non_on_base_events = [
    "strikeout",
    "field_out",
    "sac_fly",
    "field_error",
    "fielders_choice",
    "force_out",
    "grounded_into_double_play",
    "double_play",
    "strikeout_double_play",
    "fielders_choice_out",
    "triple_play",
    "sac_fly_double_play",
]

def obp(data: DataFrame) -> float:
    """
    Calculate OBP for a dataset of pitches.
    They should already be filtered to whatever player(s) you want to analyze.

    Note that statcast does NOT track intentional walks, so they are not counted here.
    """
    on = data[data["events"].isin(on_base_events)]
    not_on = data[data["events"].isin(non_on_base_events)]
    if len(on) == 0 or len(not_on) == 0:
        return 0.0
    return len(on) / (len(on) + len(not_on))

slg_weights = {
    "strikeout" : 0,
    "field_out" : 0,
    "single" : 1,
    "double" : 2,
    "force_out" : 0,
    "fielders_choice" : 0,
    "field_error" : 0,
    "home_run" : 4,
    "grounded_into_double_play" : 0,
    "double_play" : 0,
    "strikeout_double_play" : 0,
    "fielders_choice_out" : 0,
    "triple" : 3,
    "triple_play" : 0,
}

def slg(data: DataFrame) -> float:
    """
    Calculate SLG for a dataset of pitches.
    They should already be filtered to whatever player(s) you want to analyze.
    """
    evts = data["events"]
    sum = 0
    count = 0
    for e in evts.array:
        if e in slg_weights.keys():
            count += 1
            sum += slg_weights[e]
    if count == 0:
        return 0.0
    return float(sum) / float(count) 


def evs(data: DataFrame) -> Series:
    """Get array of exit velocities for a dataset of pitches.
    They should already be filtered to whatever player(s) you want to analyze."""
    balls_in_play = data[(data['events'].notnull() & data['launch_speed'].notnull())]
    return balls_in_play['launch_speed']

def batter_ids(data: DataFrame) -> numpy.ndarray:
    """Get a Series of every unique batter ID for a dataset."""
    return data["batter"].unique()


def pitcher_ids(data: DataFrame) -> numpy.ndarray:
    """Get a Series of every unique pitcher ID for a dataset."""
    return data["pitcher"].unique()


def pitch_types(data: DataFrame) -> numpy.ndarray:
    return data["pitch_name"].unique()
