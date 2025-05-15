import pandas as pd
from src.ga.scheduler import genetic_algorithm
from src.utils.visualizer import visualize_schedule
from src.utils.helper import sort_schedule , parse_input_data



if __name__ == "__main__":
    # Load input data

    with open("data\\data.json", "r") as f:
        constraints = parse_input_data(f)

    crossovar_method = int(input("Enter crossover method (1 for PMX, 2 for Order): "))
    if crossovar_method == 1:
        crossover_method = "PMX_Crossover"
    elif crossovar_method == 2:
        crossover_method = "order_crossover"
    else:
        raise ValueError("Invalid crossover method selected.")
    mutation_method = int(input("Enter mutation method (1 for Random, 2 for Swapping): "))
    if mutation_method == 1:
        mutation_method = "attribute_level_mutation"
    elif mutation_method == 2:
        mutation_method = "swap_mutation"
    else:
        raise ValueError("Invalid mutation method selected.")
    survivor_strategy = int(input("Enter survivor strategy (1 for elitism, 2 for genitor): "))
    if survivor_strategy == 1:  
        survivor_strategy = "elitism"
    elif survivor_strategy == 2:
        survivor_strategy = "genitor"
    else:
        raise ValueError("Invalid survivor strategy selected.")
    
    selection_method = int(input("Enter Selection method (1 for Tournament, 2 for Rank Based): "))
    if selection_method == 1:
        selection_method = "tournament_selection"
    elif selection_method == 2:
        selection_method = "rank_based_selection"
    else:
        raise ValueError("Invalid Selection method selected.")
    
    population_size = int(input("Enter population size: "))
    generations_size = int(input("Enter generations size: "))

    best_schedule, best_fitness, venue_violations, rest_period_violations, time_violations_details, generations_graph = genetic_algorithm(constraints, population_size=population_size, generations_size=generations_size, crossover_method=crossover_method, mutation_method=mutation_method,selection_method=selection_method,survivor_strategy=survivor_strategy)

    print(f"Best fitness: {best_fitness}")
    print(f"Venue violations: {venue_violations}")
    print(f"Rest period violations: {rest_period_violations}")


    df = pd.DataFrame(best_schedule, columns=["Team1", "Team2", "Venue", "Day", "Time Slot", "Week"])


    df['Team1'] = df['Team1'].apply(lambda x: x.get('TeamName') if isinstance(x, dict) else x)
    df['Team2'] = df['Team2'].apply(lambda x: x.get('TeamName') if isinstance(x, dict) else x)
    df['Venue'] = df['Venue'].apply(lambda x: x.get('VenueName') if isinstance(x, dict) else x)



    df.to_csv(f"best_schedule.csv", index=False)

    # Visualize the schedule
    visualize_schedule(sort_schedule(best_schedule), venue_violations, rest_period_violations, constraints)
