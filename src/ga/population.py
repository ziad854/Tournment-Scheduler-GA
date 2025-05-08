import numpy as np
import random




def initialize_population(constraints, population_size ):
    time_slots = constraints['time_slots']
    days = constraints['days']
    venues = constraints['venues']
    print(f"Venues: {venues}")
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


"""def validate_match(team1, team2, venue, day, time_slot, individual, constraints):
    '''
    Validates if a match can be added without violating constraints.
    '''
    for scheduled_match in individual:
        scheduled_team1, scheduled_team2, scheduled_venue, scheduled_day, scheduled_time_slot = scheduled_match
        
        # Check if teams are already scheduled at the same time
        if day == scheduled_day and time_slot == scheduled_time_slot:
            if team1 in (scheduled_team1, scheduled_team2) or team2 in (scheduled_team1, scheduled_team2):
                return False
        
        # Check if venue is already booked
        if venue == scheduled_venue and day == scheduled_day and time_slot == scheduled_time_slot:
            return False
    
    # Add additional constraints here (e.g., rest periods, specific venue preferences)
    return True
    # def __repr__(self):
    #     return f"Schedule({self.schedule}) """""