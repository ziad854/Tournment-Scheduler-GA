import numpy as np

class Schedule:
    def __init__(self, teams, venues, constraints):
        self.teams = teams
        self.venues = venues
        self.constraints = constraints
        self.schedule = self._initialize_schedule()

    def _initialize_schedule(self):
        # Randomly initialize a schedule (round-robin example)
        num_matches = len(self.teams) * (len(self.teams) - 1) // 2  # Total matches in round-robin
        return np.random.permutation(num_matches)

    def __repr__(self):
        return f"Schedule({self.schedule})"