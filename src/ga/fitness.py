def count_venue_conflicts(schedule, constraints):
    """
    Calculate the number of venue conflicts in the schedule.
    :param schedule: The schedule to evaluate.
    :param constraints: The constraints dictionary containing venue availability.
    :return: The number of venue conflicts.
    """
    # Example schedule representation: [(team1, team2, venue_id, day, timeslot), ...]
    conflicts = 0
    venue_availability = constraints.get("venue_availability", {})

    # Group matches by venue and day
    venue_day_map = {}
    for match in schedule:
        _, _, venue_id, day, timeslot = match
        if (venue_id, day) not in venue_day_map:
            venue_day_map[(venue_id, day)] = []
        venue_day_map[(venue_id, day)].append(timeslot)

    # Check for overlapping timeslots at the same venue on the same day
    for (venue_id, day), timeslots in venue_day_map.items():
        if day not in venue_availability.get(str(venue_id), []):
            # Venue is not available on this day
            conflicts += len(timeslots)
        else:
            # Check for overlapping timeslots
            timeslot_counts = {}
            for timeslot in timeslots:
                if timeslot not in timeslot_counts:
                    timeslot_counts[timeslot] = 0
                timeslot_counts[timeslot] += 1

            # Count conflicts (more than one match in the same timeslot)
            conflicts += sum(count - 1 for count in timeslot_counts.values() if count > 1)

    return conflicts


def count_rest_violations(schedule, constraints):
    """
    Count the number of rest period violations in the schedule.

    :param schedule: The schedule to evaluate.
                     Example: [(team1, team2, venue_id, day, timeslot), ...]
    :param constraints: The constraints dictionary containing rest period rules.
    :return: The number of rest period violations.
    """
    rest_periods = constraints.get("rest_periods", {})
    min_rest_hours = rest_periods.get("minimum_hours", 24)

    # Create a dictionary to track the last match for each team
    last_played = {}

    violations = 0

    # Sort matches by day and timeslot to process in chronological order
    # Assume `day` and `timeslot` can be sorted lexicographically
    sorted_schedule = sorted(schedule, key=lambda x: (x[3], x[4]))

    for match in sorted_schedule:
        team1, team2, _, day, timeslot = match

        # Calculate time passed for team1
        if team1 in last_played:
            last_day, last_timeslot = last_played[team1]
            hours_passed = calculate_time_difference(last_day, last_timeslot, day, timeslot)
            if hours_passed < min_rest_hours:
                violations += 1

        # Calculate time passed for team2
        if team2 in last_played:
            last_day, last_timeslot = last_played[team2]
            hours_passed = calculate_time_difference(last_day, last_timeslot, day, timeslot)
            if hours_passed < min_rest_hours:
                violations += 1

        # Update last played time for both teams
        last_played[team1] = (day, timeslot)
        last_played[team2] = (day, timeslot)

    return violations


def calculate_time_difference(day1, timeslot1, day2, timeslot2):
    """
    Calculate the time difference in hours between two matches.
    This is a helper function to determine the time difference based on days and timeslots.

    :param day1: The first match day (e.g., "Monday").
    :param timeslot1: The first match timeslot (e.g., "09:00-11:00").
    :param day2: The second match day (e.g., "Tuesday").
    :param timeslot2: The second match timeslot (e.g., "14:00-16:00").
    :return: The time difference in hours.
    """
    # Mapping of days to their order in the week
    day_order = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }

    # Calculate day difference
    day_diff = day_order[day2] - day_order[day1]

    # Parse timeslot hours
    start_hour1 = int(timeslot1.split('-')[0].split(':')[0])
    end_hour1 = int(timeslot1.split('-')[1].split(':')[0])
    mid_hour1 = (start_hour1 + end_hour1) // 2  # Approximate match time midpoint

    start_hour2 = int(timeslot2.split('-')[0].split(':')[0])
    end_hour2 = int(timeslot2.split('-')[1].split(':')[0])
    mid_hour2 = (start_hour2 + end_hour2) // 2  # Approximate match time midpoint

    # Calculate time difference in hours
    return day_diff * 24 + (mid_hour2 - mid_hour1)

from collections import defaultdict

def count_time_imbalances(schedule):
    """
    Count time imbalances for teams based on match times.
    :param schedule: The schedule to evaluate.
                     Example: [(team1, team2, venue_id, day, timeslot), ...]
    :return: A score representing time imbalances (higher score = more imbalances).
    """
    # Dictionary to track time slots for each team
    team_time_slots = defaultdict(list)

    # Populate the time slots for each team
    for match in schedule:
        team1, team2, _, _, timeslot = match
        team_time_slots[team1].append(timeslot)
        team_time_slots[team2].append(timeslot)

    # Calculate imbalance for each team
    imbalance_score = 0
    for team, timeslots in team_time_slots.items():
        # Count the frequency of each timeslot
        timeslot_frequency = defaultdict(int)
        for timeslot in timeslots:
            timeslot_frequency[timeslot] += 1

        # A perfectly balanced schedule would have similar frequencies across all timeslots
        avg_frequency = len(timeslots) / len(timeslot_frequency)
        imbalance = sum(abs(freq - avg_frequency) for freq in timeslot_frequency.values())
        imbalance_score += imbalance

    return imbalance_score

def evaluate_fitness(schedule, constraints):
    """
    Fitness function to evaluate the quality of a schedule.
    :param schedule: The schedule to evaluate.
    :param constraints: Constraints to consider.
    :return: Fitness score (higher is better).
    """
    score = 0

    # Example: Minimize venue conflicts
    score -= count_venue_conflicts(schedule, constraints)

    # Example: Ensure fair rest periods
    score -= count_rest_violations(schedule, constraints)

    # Example: Balance game times
    score -= count_time_imbalances(schedule)

    return score