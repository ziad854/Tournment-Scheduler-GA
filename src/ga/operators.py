import numpy as np

def crossover(parent1, parent2):
    """
    Single-point crossover for schedules.
    """
    point = np.random.randint(1, len(parent1.schedule) - 1)
    child1 = np.concatenate((parent1.schedule[:point], parent2.schedule[point:]))
    child2 = np.concatenate((parent2.schedule[:point], parent1.schedule[point:]))
    return child1, child2

def mutate(schedule, mutation_rate=0.1):
    """
    Swap mutation for schedules.
    """
    for i in range(len(schedule)):
        if np.random.rand() < mutation_rate:
            j = np.random.randint(0, len(schedule))
            schedule[i], schedule[j] = schedule[j], schedule[i]
    return schedule

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