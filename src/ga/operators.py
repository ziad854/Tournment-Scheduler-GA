import numpy as np
import random
# random.seed(42)  

def tournament_selection(population, fitness_scores, tournament_size=5):
    """
    Selects parents from the population using tournament selection.

    :param population: List of individuals in the current population.
    :param fitness_scores: List of fitness scores corresponding to the population.
    :param tournament_size: Number of individuals to compete in each tournament.
    :return: List of selected parents.
    """
    if tournament_size > len(population):
        raise ValueError("Tournament size cannot exceed population size.")

    selected_parents = []

    for _ in range(len(population)):
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        tournament = [(population[i], fitness_scores[i]) for i in tournament_indices]

        # Select the individual with the highest fitness score
        winner = max(tournament, key=lambda x: x[1])
        selected_parents.append(winner[0])

    return selected_parents



def rank_based_selection(population, fitness_scores, selection_pressure=1.5):
    """
    Selects parents from the population using rank-based selection.
    
    In rank-based selection, individuals are selected based on their rank
    rather than their actual fitness values, which helps maintain selection 
    pressure even when fitness values converge.
    
    :param population: List of individuals in the current population.
    :param fitness_scores: List of fitness scores corresponding to the population.
    :param selection_pressure: A value between 1.0 and 2.0 that determines the selection pressure.
                              Higher values favor higher-ranked individuals more strongly.
    :return: List of selected parents.
    """
    if not (1.0 <= selection_pressure <= 2.0):
        raise ValueError("Selection pressure must be between 1.0 and 2.0")
        
    # Create list of (individual, fitness) pairs
    population_with_fitness = list(zip(population, fitness_scores))
    
    sorted_population = sorted(population_with_fitness, key=lambda x: x[1], reverse=True)
    
    sorted_individuals = [ind for ind, _ in sorted_population]
    
    # Calculate selection probabilities based on rank
    n = len(population)
    ranks = np.arange(1, n+1)
    
    probs = (2 - selection_pressure) / n + (2 * (ranks - 1) * (selection_pressure - 1)) / (n * (n - 1))
    
    probs = np.flip(probs)
    
    probs = probs / np.sum(probs)
    
    selected_indices = np.random.choice(n, size=n, p=probs, replace=True)
    selected_parents = [sorted_individuals[i] for i in selected_indices]
    
    return selected_parents





def order_crossover(parent1, parent2): 
 
    assert len(parent1) == len(parent2)


    size = len(parent1)
    

    start, end = sorted(random.sample(range(size), 2))

    child1 = [None] * size
    child2 = [None] * size

    # Copy the segment from parent1 into child1 and from parent2 into child2
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    # Fill child1 using elements from parent2 that are not already in child1
    p2_index = end
    for i in range(size):
        if child1[i] is None:  # Find the first empty position in child1
            while parent2[p2_index % size] in child1:
                p2_index += 1
            child1[i] = parent2[p2_index % size]
            p2_index += 1

    # Fill child2 using elements from parent1 that are not already in child2
    p1_index = end
    for i in range(size):
        if child2[i] is None:  # Find the first empty position in child2
            while parent1[p1_index % size] in child2:
                p1_index += 1
            child2[i] = parent1[p1_index % size]
            p1_index += 1

    for i in range(size):
        child1[i] = (parent1[i][0], parent1[i][1], child1[i][2], child1[i][3], child1[i][4], child1[i][5])
        child2[i] = (parent2[i][0], parent2[i][1], child2[i][2], child2[i][3], child2[i][4], child2[i][5]) 
    return child1, child2






def PMX_Crossover (parent1, parent2): 
    """
    Partially Mapped Crossover (PMX) for genetic algorithms.

    :param parent1: The first parent (list of genes).
    :param parent2: The second parent (list of genes).
    :return: Two offspring generated from the parents.
    """
    assert len(parent1) == len(parent2)

    size = len(parent1)

    start, end = sorted(random.sample(range(size), 2))

    child1 = parent1[:]
    child2 = parent2[:]

    child1[start:end] = parent2[start:end]
    child2[start:end] = parent1[start:end]

    for i in range(start, end):
        gene = parent2[i]
        if gene in child1[start:end]:
            continue
        while gene in child1:
            gene = parent2[parent1.index(gene)]
        child1[child1.index(parent2[i])] = gene

    for i in range(start, end):
        gene = parent1[i]
        if gene in child2[start:end]:
            continue
        while gene in child2:
            gene = parent1[parent2.index(gene)]
        child2[child2.index(parent1[i])] = gene
    
    for i in range(size):
        child1[i] = (parent1[i][0], parent1[i][1], child1[i][2], child1[i][3], child1[i][4], child1[i][5])
        child2[i] = (parent2[i][0], parent2[i][1], child2[i][2], child2[i][3], child2[i][4], child2[i][5])   

    return child1, child2




def elitism (old_population, offspring, fitness_old, fitness_offspring, elite_size=20):
    """
    Survivor selection using elitism with random replacement.

    :param old_population: The current population (list of individuals).
    :param offspring: The offspring generated in the current generation.
    :param fitness_old: Fitness values of the old population.
    :param fitness_offspring: Fitness values of the offspring.
    :param elite_size: Number of top individuals to preserve.
    :return: The new population for the next generation.
    """
    combined_population = old_population + offspring
    combined_fitness = fitness_old + fitness_offspring

    sorted_indices = sorted(range(len(combined_fitness)), key=lambda i: combined_fitness[i], reverse=True)
    sorted_population = [combined_population[i] for i in sorted_indices]

    new_population = sorted_population[:elite_size]

    remaining_slots = len(old_population) - elite_size
    random_indices = random.sample(range(elite_size, len(sorted_population)), remaining_slots)
    new_population.extend([sorted_population[i] for i in random_indices])

    return new_population



def genitor (old_population, offspring, fitness_old, fitness_offspring):
    combined = list(zip(old_population + offspring, fitness_old + fitness_offspring))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    survivors = [ind for ind, _ in sorted_combined[:len(old_population)]]
    return survivors




def attribute_level_mutation(data, individual, mutation_rate=0.1):

    """
    Mutates the `day`, `venue`, `time slot` and `week` attributes of a match in the individual's schedule.

    :param individual: A list of matches (each match is a tuple of attributes).
    :param mutation_rate: The probability of mutating a match.
    :return: The mutated individual.
    """
    possible_days = data['days']
    possible_venues = data['venues']
    possible_weeks = data['weeks']
    possible_time_slots = data['time_slots']

    for idx, _ in enumerate(individual):
        if random.random() < mutation_rate: 
            match = individual[idx]
            

            new_day = random.choice(possible_days)
            
            new_venue = random.choice(possible_venues)
            
            new_week = random.choice(possible_weeks)

            new_time_slot = random.choice(possible_time_slots)

            individual[idx] = (
                match[0], # Keep team 1 unchanged
                match[1], # Keep team 2 unchanged
                new_venue,  
                new_day, 
                new_time_slot,  
                new_week  
            )

    return individual




def swap_mutation(individual, mutation_rate=0.1):
    """
    Performs a swap mutation on an individual's schedule.

    :param individual: A list of matches (each match is a tuple of attributes).
    :param mutation_rate: The probability of performing a mutation.
    :return: The mutated individual.
    """
    for _ in range(len(individual)):
        if random.random() < mutation_rate:

            idx1 = random.randint(0, len(individual) - 1)
            idx2 = random.randint(0, len(individual) - 1)


            while idx1 == idx2:
                idx2 = random.randint(0, len(individual) - 1)

            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]



    return individual


