import numpy as np
import random

random.seed(42)  


import numpy as np

def crossover(parent1, parent2):
    """
    Perform uniform crossover between two parents while preserving team pairings.

    :param parent1: The first parent's schedule (list of matches).
    :param parent2: The second parent's schedule (list of matches).
    :return: Two offspring schedules as lists.
    """
    assert len(parent1) == len(parent2), "Parents must have the same number of matches"

    child1 = []
    child2 = []


    for match1, match2 in zip(parent1, parent2):
        # Ensure the teams are the same in both matches (teams are fixed and won't change)



        # Perform uniform crossover for non-team attributes
        new_venue1, new_venue2 = (match1[2], match2[2]) if np.random.rand() < 0.5 else (match2[2], match1[2])
        new_day1, new_day2 = (match1[3], match2[3]) if np.random.rand() < 0.5 else (match2[3], match1[3])
        # new_time_slot1, new_time_slot2 = (match1[4], match2[4]) if np.random.rand() < 0.5 else (match2[4], match1[4])
        new_week1, new_week2 = (match1[5], match2[5]) if np.random.rand() < 0.5 else (match2[5], match1[5])

        # Construct offspring matches with preserved teams
        child1.append((match1[0], match1[1], new_venue1, new_day1, match1[4],  new_week1))
        child2.append((match2[0], match2[1], new_venue2, new_day2, match2[4], new_week2))

    return child1, child2



def mutate(data, individual, mutation_rate=0.1):
    """
    Mutates the `day`, `venue`, and `week` attributes of a match in the individual's schedule.

    :param individual: A list of matches (each match is a tuple of attributes).
    :param mutation_rate: The probability of mutating a match.
    :return: The mutated individual.
    """
    # Possible values for mutation
    possible_days = data['days']
    possible_venues = data['venues']
    possible_weeks = data['weeks']

    for idx in range(len(individual)):
        if random.random() < mutation_rate:  # Only mutate with the given probability
            # Get the current match
            match = individual[idx]

            # Mutate day
            new_day = random.choice(possible_days)
            
            # Mutate venue
            new_venue = random.choice(possible_venues)
            
            # Mutate week
            new_week = random.choice(possible_weeks)

            # Update the match while keeping teams unchanged
            individual[idx] = (
                match[0],  # Team 1
                match[1],  # Team 2
                new_venue,  # New venue
                new_day,  # New day
                match[4],  # Keep time slot unchanged
                new_week   # New week
            )

    return individual

def select_parents(population, fitness_scores, tournament_size=100):
    """
    Selects parents from the population using tournament selection.

    :param population: List of individuals in the current population.
    :param fitness_scores: List of fitness scores corresponding to the population.
    :param tournament_size: Number of individuals to compete in each tournament.
    :return: List of selected parents.
    """
    selected_parents = []

    for _ in range(len(population)):
        # Randomly select individuals for the tournament
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        tournament = [(population[i], fitness_scores[i]) for i in tournament_indices]

        # Select the individual with the highest fitness score
        winner = max(tournament, key=lambda x: x[1])
        selected_parents.append(winner[0])

    return selected_parents