from collections import defaultdict
import pandas as pd
from collections import defaultdict
from datetime import timedelta

def analyze_schedule(schedule):
    """
    Analyze the tournament schedule for validity.

    :param schedule: The schedule to evaluate.
                     Example: [({'TeamID': 1, 'TeamName': 'Team Alpha'}, {'TeamID': 4, 'TeamName': 'Team Delta'}, 
                               {'VenueID': 3, 'VenueName': 'Stadium C'}, 'Monday', '09:00-11:00', '1'), ...]
    :return: A tuple containing:
             - A boolean indicating if every team plays every other team exactly once.
             - A boolean indicating if no team plays multiple matches at the same time.
    """
    # Check that every team plays every other team exactly once
    team_matches = defaultdict(set)
    for match in schedule:
        team1, team2, _, _, _, _ = match
        team_matches[team1['TeamID']].add(team2['TeamID'])
        team_matches[team2['TeamID']].add(team1['TeamID'])

    all_teams = set(team_matches.keys())
    all_played_all = all(all_teams == opponents for opponents in team_matches.values())

    # Check that no team plays multiple matches at the same time
    team_time_slots = defaultdict(list)
    for match in schedule:
        team1, team2, _, _, timeslot, _ = match
        team_time_slots[team1['TeamID']].append(timeslot)
        team_time_slots[team2['TeamID']].append(timeslot)

    no_simultaneous_matches = all(len(set(timeslots)) == len(timeslots) for timeslots in team_time_slots.values())

    return all_played_all, no_simultaneous_matches

from operator import itemgetter

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

from datetime import datetime, timedelta

def day_to_date(day, week):
    """
    Convert a day string (e.g., "Monday", "Tuesday") and week number into a datetime object.
    Assumes the first day of the schedule is a Monday.

    :param day: The day of the week as a string (e.g., "Monday").
    :param week: The week number as a string (e.g., "1").
    :return: A datetime object representing the date.
    """
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if day not in days_of_week:
        raise ValueError(f"Invalid day: {day}")

    base_date = datetime(2025, 5, 5)  # Start of the schedule (Monday, May 5th, 2025)
    day_index = days_of_week.index(day)

    week_offset = (int(week) - 1) * 7
    return base_date + timedelta(days=day_index + week_offset)


def detect_violations(schedule,constraints):
    """
    Detect violations in the tournament schedule.

    :param schedule: A list of matches, where each match is a tuple:
                     (team1, team2, venue, day, timeslot, week).
    :param min_rest_hours: Minimum rest period in hours for teams.
    :return: A dictionary containing the detected violations.
    """
    venue_date_map = {}
    team_schedule_map = {}
    violations = {
        "venue_conflicts": [],
        "team_overlaps": [],
        "rest_violations": []
    }

    min_rest_hours = constraints.get("rest_periods", {}).get("minimum_hours", 72)    

    for match in schedule:
        team1 = match[0]["TeamID"]
        team2 = match[1]["TeamID"]
        venue_id = match[2]["VenueID"]
        day = match[3]
        timeslot = match[4]
        week = match[5]

        # Calculate the actual datetime for the match
        match_date = day_to_date(day, week)

        # Venue conflict check
        venue_key = (venue_id, match_date)
        if venue_key not in venue_date_map:
            venue_date_map[venue_key] = []
        else:
            violations["venue_conflicts"].append(match)
        venue_date_map[venue_key].append((team1, team2))

        # Team overlap check
        for team in [team1, team2]:
            if team not in team_schedule_map:
                team_schedule_map[team] = []
            else:
                for previous_match in team_schedule_map[team]:
                    if previous_match[0] == match_date and previous_match[1] == timeslot:
                        violations["team_overlaps"].append(match)
            team_schedule_map[team].append((match_date, timeslot))

        # Rest violation check
        for team in [team1, team2]:
            for previous_match in team_schedule_map[team]:
                time_difference = (match_date - previous_match[0]).total_seconds() / 3600
                if time_difference < min_rest_hours:
                    violations["rest_violations"].append(match)

    return violations



import pandas as pd
from collections import defaultdict

def count_schedule_violations(df):
    """
    Count schedule violations, including venue usage violations and team match interval violations.
    
    :param df: A pandas DataFrame with columns ['Week', 'Day', 'Venue', 'Team 1', 'Team 2'].
    :return: A dictionary containing the counts for each type of violation and the total violations.
    """
    # Map day names to index values for calculations
    day_to_index = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2,
        "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
    }

    # Track venue usage for each week and day
    venue_usage = defaultdict(set)  # {(week, day): set of venues}
    venue_violations = 0

    # Track matches for each team
    team_matches = defaultdict(list)  # {team: list of (week, day_index)}

    # Process each row in the DataFrame
    for _, row in df.iterrows():
        week = int(row['Week'])
        day = row['Day']
        venue = row['Venue']
        team1 = row['Team 1']
        team2 = row['Team 2']
        day_index = day_to_index[day]

        # Check for venue usage violations
        if venue in venue_usage[(week, day)]:
            venue_violations += 1
        else:
            venue_usage[(week, day)].add(venue)

        # Add matches to both teams
        team_matches[team1].append((week, day_index))
        team_matches[team2].append((week, day_index))

    # Calculate match spacing violations
    match_spacing_violations = 0

    for team, matches in team_matches.items():
        # Convert matches to absolute day counts: (week * 7 + day_index)
        match_days = sorted([week * 7 + day for (week, day) in matches])
        for i in range(1, len(match_days)):
            if match_days[i] - match_days[i - 1] < 3:
                match_spacing_violations += 1
                break  # Count only one violation per team

    # Calculate total violations
    total_violations = venue_violations + match_spacing_violations

    # Return the results
    return {
        "Venue Violations": venue_violations,
        "Team Match Interval Violations": match_spacing_violations,
        "Total Violations": total_violations
    }