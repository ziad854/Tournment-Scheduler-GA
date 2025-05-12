import numpy as np
import random

random.seed(42)  # For reproducibility


def initialize_population(constraints, population_size ):
    time_slots = constraints['time_slots']
    days = constraints['days']
    venues = constraints['venues']
    teams = constraints['teams']
    weeks = constraints['weeks']
    population = []
    total_matches = [(team1, team2) for i, team1 in enumerate(teams) for j, team2 in enumerate(teams) if i < j]
    
    for _ in range(population_size):
        individual = []
        random.shuffle(total_matches)  # Shuffle matches for diversity
        
        for match in total_matches:
            team1, team2 = match
            time_slot = random.choice(time_slots)
            venue = random.choice(venues)
            day = random.choice(days)
            #time_slot = random.choice(time_slots)
            week = random.choice(weeks)
            
            # Ensure constraints are respected (e.g., venue availability, no conflicts)
            # if validate_match(team1, team2, venue, day, time_slot, individual, constraints):
            individual.append((team1, team2, venue, day, time_slot,week))
        
        population.append(individual)
    
    return population


