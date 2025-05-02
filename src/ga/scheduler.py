from src.ga.population import Schedule
from src.ga.fitness import evaluate_fitness
from src.ga.operators import crossover, mutate
from src.ga.operators import select_parents

def genetic_algorithm(teams, venues, constraints, generations=100, population_size=50):
    """
    Run the Genetic Algorithm to generate tournament schedules.
    """
    # Initialize population
    population = [Schedule(teams, venues, constraints) for _ in range(population_size)]

    for generation in range(generations):
        # Evaluate fitness
        fitness_scores = [evaluate_fitness(ind.schedule, constraints) for ind in population]

        # Select parents
        selected = select_parents(population, fitness_scores)

        # Generate new population through crossover
        new_population = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([child1, child2])

        # Mutate the schedules and wrap them back into Schedule objects
        population = [
            Schedule(teams, venues, constraints)._replace_schedule(mutate(schedule))
            for schedule in new_population
        ]

        # Log the best fitness
        best_fitness = max(fitness_scores)
        print(f"Generation {generation}: Best Fitness = {best_fitness}")

    return population