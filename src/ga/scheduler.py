from src.ga.fitness import evaluate_fitness
from src.ga.operators import *
from src.ga.population import initialize_population



def genetic_algorithm(constraints, population_size, generations_size, 
                      crossover_method, mutation_method,selection_method, survivor_strategy="elitism"):
    # Initialize population
    population = initialize_population(constraints, population_size)
    fitness_scores = [evaluate_fitness(ind, constraints)[0] for ind in population]

    best_fitness = max(fitness_scores)
    idx_best = fitness_scores.index(best_fitness)
    generations_graph = [best_fitness]
    generation = 0

    while best_fitness != 0 and generation < generations_size:
        # --- Parent Selection ---
        match selection_method:
            case "tournament_selection":
                selected = tournament_selection(population, fitness_scores, tournament_size=population_size // 2)
            case "rank_based_selection":
                selected = rank_based_selection(population, fitness_scores, selection_pressure=1.2)
            case _:
                raise ValueError(f"Unknown selection method: {selection_method}")


        # --- Crossover ---
        new_population = []
        for i in range(0, len(selected) - 1, 2):
            parent1, parent2 = selected[i], selected[i+1]
            match crossover_method:
                case "order_crossover":
                    child1, child2 = order_crossover(parent1, parent2)
                case "PMX_Crossover":
                    child1, child2 = PMX_Crossover(parent1, parent2)
                case _:
                    raise ValueError(f"Unknown crossover type: {crossover_method}")
            new_population.extend([child1, child2])

        # --- Mutation ---
        match mutation_method:
            case "attribute_level_mutation":
                mutated_population = [attribute_level_mutation(constraints, ind) for ind in new_population]
            case "swap_mutation":
                mutated_population = [swap_mutation(ind) for ind in new_population]
            case _:
                raise ValueError(f"Unknown mutation type: {mutation_method}")

        # --- Evaluate Fitness ---
        offspring_fitness = [evaluate_fitness(ind, constraints)[0] for ind in mutated_population]

        # --- Survivor Selection ---
        match survivor_strategy:
            case "elitism":
                population = elitism(population, mutated_population, fitness_scores, offspring_fitness)
                fitness_scores = [evaluate_fitness(ind, constraints)[0] for ind in population]
            case "genitor":
                population = genitor(population, mutated_population, fitness_scores, offspring_fitness)
                fitness_scores = [evaluate_fitness(ind, constraints)[0] for ind in population]
            case _:
                population = mutated_population
                fitness_scores = offspring_fitness

        # --- Track Best ---
        generation_best_fitness = max(fitness_scores)
        if generation_best_fitness > best_fitness:
            best_fitness = generation_best_fitness
            idx_best = fitness_scores.index(best_fitness)

        generations_graph.append(best_fitness)
        print(f"Generation {generation}: Best Fitness = {best_fitness}")
        generation += 1
    score, venue_violations, rest_period_violations = evaluate_fitness(population[idx_best], constraints)
    return population[idx_best],score, venue_violations, rest_period_violations, generations_graph
