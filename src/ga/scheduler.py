from src.ga.population import initialize_population
from src.ga.fitness import evaluate_fitness
from src.ga.operators import crossover, mutate, select_parents


def genetic_algorithm(constraints,population_size=500):
    # Initialize population
    population = initialize_population(constraints, population_size )

    init_eval = [evaluate_fitness(ind, constraints) for ind in population]
    generation = 0
    while init_eval != 0 :# and generation < 100:
        # Evaluate fitness
        fitness_scores = [evaluate_fitness(ind, constraints) for ind in population]
        init_eval = fitness_scores
        # Select parents
        selected = select_parents(population, fitness_scores)

        # Generate new population
        new_population = []
        for i in range(0, len(selected)-1, 2):
            parent1, parent2 = selected[i], selected[i+1]
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([child1, child2])

        # Mutate
        population = [mutate(ind) for ind in new_population]

        # Replace old population
        population = new_population

        # Log best fitness
        best_fitness = max(fitness_scores)
        print(f"Generation {generation}: Best Fitness = {best_fitness}")
        generation += 1

    return population


