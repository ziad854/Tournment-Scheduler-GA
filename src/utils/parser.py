import pandas as pd
import json

def parse_input_data(teams_file, venues_file, constraints_file):
    teams = pd.read_csv(teams_file)
    venues = pd.read_csv(venues_file)
    with open(constraints_file, "r") as f:
        constraints = json.load(f)
    return teams, venues, constraints