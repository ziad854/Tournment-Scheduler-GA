import numpy as np
import random

random.seed(42)  


def crossover(parent1, parent2):
    """
    Single-point crossover for schedules. Ensures that the offspring maintain
    the integrity of the teams in the matches by excluding teams from the crossover process.

    :param parent1: The first parent's schedule.
    :param parent2: The second parent's schedule.
    :return: Two offspring schedules as numpy arrays.
    """
    # Ensure both parents have the same length
    assert len(parent1) == len(parent2), "Parents must have the same number of matches"

    # Randomly select a crossover point
    point = np.random.randint(1, len(parent1) - 1)

    # Create initial offspring by combining parts of the parents for non-team attributes
    child1 = []
    child2 = []

    for i in range(len(parent1)):
        # Extract teams (remain unchanged)
        team1_1, team2_1 = parent1[i][0], parent1[i][1]
        team1_2, team2_2 = parent2[i][0], parent2[i][1]

        # Extract non-team attributes
        if i < point:
            # Take non-team attributes from parent1 for child1 and parent2 for child2
            non_team_attrs1 = parent1[i][2:]
            non_team_attrs2 = parent2[i][2:]
        else:
            # Take non-team attributes from parent2 for child1 and parent1 for child2
            non_team_attrs1 = parent2[i][2:]
            non_team_attrs2 = parent1[i][2:]

        # Construct offspring matches
        child1.append((team1_1, team2_1, *non_team_attrs1))
        child2.append((team1_2, team2_2, *non_team_attrs2))

    # Convert offspring to numpy arrays for consistency
    return np.array(child1), np.array(child2)


def mutate(individual):
    """
    Mutates an individual schedule by swapping attributes (time_slot, venue, week, and day)
    between two randomly selected matches.

    :param individual: A list of matches. Example format:
                       [({'TeamID': 1, 'TeamName': 'Team Alpha'}, {'TeamID': 4, 'TeamName': 'Team Delta'}, 
                         {'VenueID': 3, 'VenueName': 'Stadium C'}, 'Monday', '09:00-11:00', '1'), ...]
    :return: None. The individual is modified in place.
    """
    # Ensure there are at least two matches to perform mutation
    if len(individual) < 2:
        return

    # Randomly select two distinct indices
    idx1, idx2 = random.sample(range(len(individual)), 2)

    # Extract the matches to be mutated
    match1 = individual[idx1]
    match2 = individual[idx2]

    # Swap the attributes
    mutated_match1 = (
        match1[0],  # team1 remains the same
        match1[1],  # team2 remains the same
        match2[2],  # Swap venue
        match2[3],  # Swap day
        match2[4],  # Swap time_slot
        match2[5]   # Swap week
    )

    mutated_match2 = (
        match2[0],  # team1 remains the same
        match2[1],  # team2 remains the same
        match1[2],  # Swap venue
        match1[3],  # Swap day
        match1[4],  # Swap time_slot
        match1[5]   # Swap week
    )

    # Update the individual with the mutated matches
    individual[idx1] = mutated_match1
    individual[idx2] = mutated_match2

def select_parents(population, fitness_scores, tournament_size=3):
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