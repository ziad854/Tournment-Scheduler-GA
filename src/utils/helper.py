import pandas as pd
import json

def parse_input_data(data_file):
    try:
        constraints = json.load(data_file)
        return constraints
    except Exception as e:
        raise RuntimeError(f"An error occurred while parsing the file {data_file}: {e}")
    


def sort_schedule(schedule):
    """
    Sort the schedule visually by week, day, and time slot.

    :param schedule: The unsorted schedule containing match details.
    :return: A sorted schedule.
    """
    # Define the order of days in a week to ensure proper sorting
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Sort the schedule by week, day, and time_slot
    sorted_schedule = sorted(
        schedule,
        key=lambda match: (
            # int(match[0]['TeamID']),  # Team 1 ID (for sorting purposes)
            # int(match[1]['TeamID']),  # Team 2 ID (for sorting purposes)
            int(match[5]),  # Week
            day_order.index(match[3]),  # Day
            match[4]  # Time slot
        )
    )
    return sorted_schedule