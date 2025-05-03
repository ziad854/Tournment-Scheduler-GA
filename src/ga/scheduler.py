from src.ga.population import initialize_population
from src.ga.fitness import evaluate_fitness
from src.ga.operators import crossover, mutate, select_parents


def genetic_algorithm(constraints,population_size):
    # Initialize population
    population = initialize_population(constraints, population_size )

    fitness_scores = [evaluate_fitness(ind, constraints) for ind in population]

    best_fitness = max(fitness_scores)
    best_generation  = population
    generation = 0
    while fitness_scores != 0  and generation < 500:
        # Evaluate fitness
        fitness_scores = [evaluate_fitness(ind, constraints) for ind in population]

        # Select parents
        selected = select_parents(population, fitness_scores)

        # Generate new population
        new_population = []
        for i in range(0, len(selected)-1, 2):
            parent1, parent2 = selected[i], selected[i+1]
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([child1, child2])

        # Mutate
        population = [mutate(constraints,ind) for ind in new_population]

        # Replace old population
        population = new_population

        # Log best fitness
        if best_fitness < max(fitness_scores):
            best_generation = population
            best_fitness = max(fitness_scores)
            print(f"New best fitness found: {best_fitness}")
        print(f"Generation {generation}: Best Fitness = {best_fitness}")

        generation += 1

    return best_generation, best_fitness


