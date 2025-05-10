from src.ga.fitness import evaluate_fitness
from src.ga.operators import crossover, mutate, select_parents
from src.ga.population import initialize_population
import pandas as pd

def genetic_algorithm(constraints,population_size , genrations_size):
    # Initialize population
    population = initialize_population(constraints, population_size )

    fitness_scores = [evaluate_fitness(ind, constraints) for ind in population]

    best_fitness = max(fitness_scores)
    best_generation  = population
    idx_best = None
    generation = 0
    while best_fitness != 0  and generation < genrations_size:


        # Select parents
        selected = select_parents(population, fitness_scores)

        # Generate new population
        new_population = []
        for i in range(0, len(selected)-1, 2):
            parent1, parent2 = selected[i], selected[i+1]
            child1, child2 = crossover(parent1, parent2)

            new_population.extend([child1,child2])

        # Mutate
        mutated_population = [mutate(constraints,ind) for ind in new_population]




        # Evaluate fitness
        fitness_scores = []
        for idx, ind in enumerate(mutated_population):
            fitness = evaluate_fitness(ind, constraints)
            if fitness > best_fitness:
                best_fitness = fitness
                idx_best = idx
            fitness_scores.append(fitness)



        # Log best fitness
        # current_best_fitness = max(fitness_scores)
        # if current_best_fitness > best_fitness:  # Update if we find a better score
        #     best_generation = mutated_population
        #     best_fitness = current_best_fitness
        #     print(f"New best fitness found: {best_fitness} at Generation {generation}")

        # Stop early if perfect fitness is achieved
        # if best_fitness == -1:
        #     print(f"Generation {generation}: Best Fitness = {best_fitness}")
        #     print(fitness_scores)
        #     return mutated_population[idx_best], best_fitness
        
        print(f"Generation {generation}: Best Fitness = {max(fitness_scores)}")

        population = mutated_population
        generation += 1

    return mutated_population[idx_best], best_fitness


