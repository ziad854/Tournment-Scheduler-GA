from datetime import datetime, timedelta
from collections import defaultdict

def count_venue_conflicts(individual, constraints):
    """
    Calculate the number of venue conflicts in the schedule.

    A conflict occurs if the same venue is scheduled for more than one match
    in the same time slot, on the same day, and in the same week.

    :param individual: The schedule to evaluate.
    :param constraints: The constraints dictionary containing venue availability.
    :return: The number of venue conflicts.
    """
    conflicts = 0

    # Group matches by venue, day, week, and timeslot
    venue_day_week_timeslot_map = {}
    for match in individual:
        _, _, venue, day, timeslot, week = match  # Unpack match details
        venue_id = venue["VenueID"]

        # Create a unique key for (venue, day, week, timeslot)
        key = (venue_id, day, week, timeslot)

        if key not in venue_day_week_timeslot_map:
            venue_day_week_timeslot_map[key] = 0
        venue_day_week_timeslot_map[key] += 1

    # Count conflicts (more than one match in the same timeslot, day, week, and venue)
    for key, count in venue_day_week_timeslot_map.items():
        if count > 1:
            conflicts += count - 1  # Add conflicts for overlapping matches

    return conflicts






def count_rest_violations(individual, constraints):
    """
    Count the number of rest period violations in the schedule.

    :param individual: The schedule to evaluate.
                       Example: [({'TeamID': 1, 'TeamName': 'Team Alpha'}, {'TeamID': 4, 'TeamName': 'Team Delta'}, venue_id, day, timeslot, week), ...]
    :param constraints: The constraints dictionary containing rest period rules.
    :return: The number of rest period violations.
    """
    rest_periods = constraints.get("rest_periods", {})
    min_rest_days = rest_periods.get("minimum_hours", 72) // 24  # Convert hours to days (3 days)

    # Create a dictionary to track the last match day for each team
    last_played = {}

    violations = 0

    # Sort matches by day and timeslot to process in chronological order
    sorted_schedule = sorted(individual, key=lambda x: (x[3], x[4]))

    for match in sorted_schedule:
        team1, team2, _, day, _, _ = match

        # Use TeamID to uniquely identify each team
        team1_id = team1['TeamID']
        team2_id = team2['TeamID']

        # Convert day to a datetime object for comparison
        current_date = day_to_date(day)

        # Check rest period for team1
        if team1_id in last_played:
            last_date = last_played[team1_id]
            days_passed = (current_date - last_date).days
            if days_passed < min_rest_days:
                violations += 1

        # Check rest period for team2
        if team2_id in last_played:
            last_date = last_played[team2_id]
            days_passed = (current_date - last_date).days
            if days_passed < min_rest_days:
                violations += 1

        # Update last played time for both teams
        last_played[team1_id] = current_date
        last_played[team2_id] = current_date

    return violations



def day_to_date(day):
    """
    Convert a day string (e.g., "Monday", "Tuesday") into a datetime object.
    Assumes the first day of the schedule is a Monday.

    :param day: The day of the week as a string.
    :return: A datetime object representing the day.
    """
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    base_date = datetime(2025, 5, 5)  # Start of the schedule (example: a Monday)
    day_index = days_of_week.index(day)
    return base_date + timedelta(days=day_index)


# def calculate_time_difference(day1, timeslot1, day2, timeslot2):
#     """
#     Calculate the time difference in hours between two matches.
#     This is a helper function to determine the time difference based on days and timeslots.
#     :param day1: The first match day (e.g., "Monday").
#     :param timeslot1: The first match timeslot (e.g., "09:00-11:00").
#     :param day2: The second match day (e.g., "Tuesday").
#     :param timeslot2: The second match timeslot (e.g., "14:00-16:00").
#     :return: The time difference in hours.
#     """
#     # Mapping of days to their order in the week
#     day_order = {
#         "Monday": 0,
#         "Tuesday": 1,
#         "Wednesday": 2,
#         "Thursday": 3,
#         "Friday": 4,
#         "Saturday": 5,
#         "Sunday": 6
#     }
#     # Calculate day difference
#     day_diff = day_order[day2] - day_order[day1]
#     # Parse timeslot hours
#     start_hour1 = int(timeslot1.split('-')[0].split(':')[0])
#     end_hour1 = int(timeslot1.split('-')[1].split(':')[0])
#     mid_hour1 = (start_hour1 + end_hour1) // 2  # Approximate match time midpoint
#     start_hour2 = int(timeslot2.split('-')[0].split(':')[0])
#     end_hour2 = int(timeslot2.split('-')[1].split(':')[0])
#     mid_hour2 = (start_hour2 + end_hour2) // 2  # Approximate match time midpoint
#     # Calculate time difference in hours
#     return day_diff * 24 + (mid_hour2 - mid_hour1)




def count_time_imbalances(individual):
    """
    Count time imbalances for teams based on match times.

    :param schedule: The schedule to evaluate.
                     Example: [({'TeamID': 1, 'TeamName': 'Team Alpha'}, {'TeamID': 4, 'TeamName': 'Team Delta'}, 
                               {'VenueID': 3, 'VenueName': 'Stadium C'}, 'Monday', '19:00-21:00', '1'), ...]
    :return: A score representing time imbalances (higher score = more imbalances).
    """
    # Dictionary to track time slots for each team
    team_time_slots = defaultdict(list)

    # Populate the time slots for each team
    for match in individual:
        team1, team2, _, _, timeslot, _ = match  # Unpack the schedule tuple
        team_time_slots[team1['TeamID']].append(timeslot)
        team_time_slots[team2['TeamID']].append(timeslot)

    # Calculate imbalance for each team
    imbalance_score = 0
    for team_id, timeslots in team_time_slots.items():
        # Count the frequency of each timeslot
        timeslot_frequency = defaultdict(int)
        for timeslot in timeslots:
            timeslot_frequency[timeslot] += 1

        # Handle edge case where no matches are scheduled for the team
        if len(timeslot_frequency) == 0:
            continue

        # A perfectly balanced schedule would have similar frequencies across all timeslots
        total_matches = len(timeslots)
        avg_frequency = total_matches / len(timeslot_frequency)

        # Calculate imbalance as deviation from the average frequency
        imbalance = sum(abs(freq - avg_frequency) for freq in timeslot_frequency.values())
        imbalance_score += imbalance

    return imbalance_score

def evaluate_fitness(individual, constraints):
    """
    Fitness function to evaluate the quality of a schedule.
    :param schedule: The schedule to evaluate.
    :param constraints: Constraints to consider.
    :return: Fitness score (higher is better).
    """
    score = 0

    # Example: Minimize venue conflicts
    score -= count_venue_conflicts(individual, constraints)

    # Example: Ensure fair rest periods
    score -= count_rest_violations(individual, constraints)

    # Example: Balance game times
    # score -= count_time_imbalances(individual)

    return score