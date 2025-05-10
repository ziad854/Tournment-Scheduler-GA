# def count_venue_conflicts(individual, constraints):
#     """
#     Calculate the number of venue conflicts in the schedule.

#     A conflict occurs if the same venue is scheduled for more than one match
#     in the same time slot, on the same day, and in the same week.

#     :param individual: The schedule to evaluate.
#     :param constraints: The constraints dictionary containing venue availability.
#     :return: The number of venue conflicts.
#     """
#     conflicts = 0

#     # Group matches by venue, day, week, and timeslot
#     venue_day_week_map = {}
#     for match in individual:
#         team1, team2, venue, day, _, week = match  # Unpack match details
#         venue_id = venue["VenueID"]

#         # Create a unique key for (venue, day, week, timeslot)
#         key = (venue_id, day, week, team1, team2,)

#         if key not in venue_day_week_map:
#             venue_day_week_map[key] = 0
#         else:
#             venue_day_week_map[key] += 1

#     # Count conflicts (more than one match in the same timeslot, day, week, and venue)
#     for key, count in venue_day_week_map.items():
#         if count > 1:
#             conflicts += count - 1  # Add conflicts for overlapping matches

#     return conflicts

# def count_venue_conflicts(individual,constraints):
#     """
#     Count venue conflicts based on the actual date instead of separate day and week.

#     :param individual: The schedule to evaluate, where each match contains:
#                        (team1, team2, venue, day, timeslot, week).
#     :return: The number of venue conflicts.
#     """
#     venue_date_map = {}
#     conflicts = 0

#     for match in individual:
#         _, _, venue, day, _, week = match  # Unpack match details
#         venue_id = venue["VenueID"]

#         # Calculate the actual date using the day and week
#         match_date = day_to_date(day, week)

#         # Create a unique key for (venue, date, timeslot, teams)
#         key = (venue_id, match_date)

#         if key not in venue_date_map:
#             venue_date_map[key] = 0
#         else:
#             venue_date_map[key] += 1

#     # Count conflicts (more than one match in the same timeslot, day, week, and venue)
#     for key, count in venue_date_map.items():
#         if count > 1:
#             conflicts += count - 1  # Add conflicts for overlapping matches

#     return conflicts


# def count_rest_violations(individual, constraints):
#     """
#     Count the number of rest period violations in the schedule.

#     :param individual: The schedule to evaluate.
#                        Example: [({'TeamID': 1, 'TeamName': 'Team Alpha'}, {'TeamID': 4, 'TeamName': 'Team Delta'}, venue_id, day, timeslot, week), ...]
#     :param constraints: The constraints dictionary containing rest period rules.
#     :return: The number of rest period violations.
#     """
#     # Fetch minimum rest days from constraints or default to 3
#     min_rest_days = 3 #constraints.get("min_rest_days", 3)

#     # Create a dictionary to track the last match day for each team
#     last_played = {}

#     violations = 0

#     # Sort matches by week, day, and timeslot to process in chronological order
#     sorted_schedule = sorted(individual, key=lambda x: (int(x[5]), x[3]))

#     for match in sorted_schedule:
#         team1, team2, _, day, _, week = match

#         # Use TeamID to uniquely identify each team
#         team1_id = team1['TeamID']
#         team2_id = team2['TeamID']

#         # Convert day and week to a datetime object for comparison
#         current_date = day_to_date(day, week)

#         # Check rest period for team1
#         if team1_id in last_played:
#             last_date = last_played[team1_id]
#             days_passed = (current_date - last_date).days
#             # print(f"Days passed for team {team1_id}: {days_passed} (last played: {last_date}, current date: {current_date})")
#             if days_passed < min_rest_days:
#                 violations += 1

#         # Check rest period for team2
#         if team2_id in last_played:
#             last_date = last_played[team2_id]
#             days_passed = (current_date - last_date).days
#             # print(f"Days passed for team {team2_id}: {days_passed} (last played: {last_date}, current date: {current_date})")
#             if days_passed < min_rest_days:
#                 violations += 1

#         # Update last played time for both teams
#         last_played[team1_id] = current_date
#         last_played[team2_id] = current_date

#     return violations

# def count_rest_violations(schedule, constraints):
#     """
#     Count rest period violations for teams.
#     :param schedule: The schedule to evaluate.
#     :param constraints: The constraints dictionary.
#     :return: The number of rest period violations.
#     """
#     min_rest_hours = constraints.get("rest_periods", {}).get("minimum_hours", 24)
#     rest_violations = 0
#     team_schedule_map = {}

#     for match in schedule:
#         team1 = match[0]["TeamID"]  # Use TeamID as the hashable key
#         team2 = match[1]["TeamID"]  # Use TeamID as the hashable key
#         _, _, _, day, timeslot, week = match

#         # Calculate the actual datetime for this match
#         match_date = day_to_date(day, week)

#         # Check rest periods for team1
#         if team1 not in team_schedule_map:
#             team_schedule_map[team1] = []
#         else:
#             for previous_match in team_schedule_map[team1]:
#                 time_difference = (match_date - previous_match).total_seconds() / 3600
#                 if time_difference < min_rest_hours:
#                     rest_violations += 1

#         team_schedule_map[team1].append(match_date)

#         # Check rest periods for team2
#         if team2 not in team_schedule_map:
#             team_schedule_map[team2] = []
#         else:
#             for previous_match in team_schedule_map[team2]:
#                 time_difference = (match_date - previous_match).total_seconds() / 3600
#                 if time_difference < min_rest_hours:
#                     rest_violations += 1

#         team_schedule_map[team2].append(match_date)

#     return rest_violations

# def count_time_imbalances(individual, constraints):
#     """
#     Count time imbalances where a team is scheduled to play more than once
#     on the same day (same week and day).
    
#     :param individual: The schedule to evaluate.
#     :return: The number of day-level scheduling conflicts per team.
#     """
#     # Dictionary to track (week, day) match counts per team
#     team_daily_schedule = defaultdict(lambda: defaultdict(int))

#     for match in individual:
#         team1, team2, _, day, _, week = match  # Unpack match
#         key = (week, day)

#         # Increment match count for each team on that (week, day)
#         team_daily_schedule[team1['TeamID']][key] += 1
#         team_daily_schedule[team2['TeamID']][key] += 1

#     # Count violations where a team has more than one match on the same day
#     imbalance_score = 0
#     for team_id, daily_counts in team_daily_schedule.items():
#         for key, count in daily_counts.items():
#             if count > 1:
#                 imbalance_score += count - 1  # Count extra matches as conflicts

#     return imbalance_score


# def day_to_date(day, week):
#     """
#     Convert a day string (e.g., "Monday", "Tuesday") and week number into a datetime object.
#     Assumes the first day of the schedule is a Monday.

#     :param day: The day of the week as a string (e.g., "Monday").
#     :param week: The week number as a string (e.g., "1").
#     :return: A datetime object representing the date.
#     """
#     days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

#     # Check if the day is valid
#     if day not in days_of_week:
#         raise ValueError(f"Invalid day: {day}")

#     base_date = datetime(2025, 5, 5)  
#     day_index = days_of_week.index(day)

#     # Calculate the date, accounting for the week number
#     week_offset = (int(week) - 1) * 7
#     return base_date + timedelta(days=day_index + week_offset)



# def validate_match(team1, team2, venue, day, time_slot, individual, constraints):
#     '''
#     Validates if a match can be added without violating constraints.
#     '''
#     for scheduled_match in individual:
#         scheduled_team1, scheduled_team2, scheduled_venue, scheduled_day, scheduled_time_slot = scheduled_match
        
#         # Check if teams are already scheduled at the same time
#         if day == scheduled_day and time_slot == scheduled_time_slot:
#             if team1 in (scheduled_team1, scheduled_team2) or team2 in (scheduled_team1, scheduled_team2):
#                 return False
        
#         # Check if venue is already booked
#         if venue == scheduled_venue and day == scheduled_day and time_slot == scheduled_time_slot:
#             return False
    
#     # Add additional constraints here (e.g., rest periods, specific venue preferences)
#     return True
#     # def __repr__(self):
#     #     return f"Schedule({self.schedule}) 