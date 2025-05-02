import numpy as np
import itertools

class Schedule:
    def __init__(self, teams, venues, constraints):
        self.teams = teams
        self.venues = venues
        self.constraints = constraints
        self.schedule = self._initialize_schedule()

    def _initialize_schedule(self):
        team_ids = self.teams["TeamID"].tolist()
        venue_ids = self.venues["VenueID"].tolist()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        timeslots = self.constraints["time_slots"]

        all_matches = list(itertools.combinations(team_ids, 2))  # Generate all possible matches
        schedule = []

        for match in all_matches:
            team1, team2 = match
            venue_id = int(np.random.choice(venue_ids))  # Ensure it's an int
            day = str(np.random.choice(days))  # Ensure it's a string
            timeslot = str(np.random.choice(timeslots))  # Ensure it's a timeslot string
            schedule.append((team1, team2, venue_id, day, timeslot))  # Append as a tuple

        return schedule

    def _replace_schedule(self, new_schedule):
        """
        Replace the schedule with a new one.
        :param new_schedule: The new schedule (list of matches).
        :return: A new Schedule object with the updated schedule.
        """
        self.schedule = new_schedule
        return self