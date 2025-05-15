import matplotlib.pyplot as plt
from itertools import product
from src.ga.scheduler import genetic_algorithm
from src.utils.helper import parse_input_data

# Define the parameter search space
crossover_methods = ["order_crossover", "PMX_Crossover"]
mutation_methods = ["attribute_level_mutation", "swap_mutation"]
survivor_strategies = ["elitism", "genitor"]
selection_methods = ["tournament_selection", "rank_based_selection"]

# Define other parameters
population_size = 200
generations_size = 100

with open("data/data.json", "r") as f:
    constraints = parse_input_data(f)
# To store the results
results = []

# Perform grid search over all parameter combinations
for crossover_method, mutation_method, survivor_strategy, selection_methods in product(crossover_methods, mutation_methods, survivor_strategies, selection_methods):
    print(f"Testing combination: Crossover = {crossover_method}, Mutation = {mutation_method}, Survivor Strategy = {survivor_strategy}, Selection = {selection_methods}")
    
    # Run the genetic algorithm
    best_individual, best_fitness, venue_violations, rest_period_violations, fitness_graph = genetic_algorithm(
        constraints, 
        population_size, 
        generations_size, 
        crossover_method, 
        mutation_method,
        selection_methods, 
        survivor_strategy
    )
    
    # Record the results
    results.append({
        "crossover_method": crossover_method,
        "mutation_method": mutation_method,
        "survivor_strategy": survivor_strategy,
        "selection_method": selection_methods,
        "best_fitness": best_fitness,
        "fitness_graph": fitness_graph
    })

# Find the best combination
best_result = max(results, key=lambda x: x["best_fitness"])

# Print the best combination
print("\nBest Combination:")
print(f"Crossover Method: {best_result['crossover_method']}")
print(f"Mutation Method: {best_result['mutation_method']}")
print(f"Survivor Strategy: {best_result['survivor_strategy']}")
print(f"Selection Method: {best_result['selection_method']}")
print(f"Best Fitness: {best_result['best_fitness']}")

# Graph the results
plt.figure(figsize=(16, 8))

for result in results:
    label = f"{result['crossover_method']} + {result['mutation_method']} + {result['survivor_strategy']} + {result['selection_method']}"
    plt.plot(result["fitness_graph"], label=label)

plt.title("Fitness Evolution for Different Parameter Combinations")
plt.xlabel("Generations")
plt.ylabel("Fitness")
plt.legend(loc="best")
plt.grid(True)
plt.show()