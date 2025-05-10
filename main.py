from src.ga.fitness import evaluate_fitness
from src.ga.scheduler import genetic_algorithm
from src.utils.parser import parse_input_data
from src.utils.visualizer import visualize_schedule
from src.utils.analsyis import *

if __name__ == "__main__":
    # Load input data
    constraints = parse_input_data("data/data.json")


    # Run GA
    best_schedule, best_fitness = genetic_algorithm(constraints, population_size=100, genrations_size=100)

    print(f"Best fitness: {best_fitness}")


    df = pd.DataFrame(best_schedule, columns=["Team1", "Team2", "Venue", "Day", "Time Slot", "Week"])

    # Extract TeamName from dictionaries
    df['Team1'] = df['Team1'].apply(lambda x: x['TeamName'] if isinstance(x, dict) else x)
    df['Team2'] = df['Team2'].apply(lambda x: x['TeamName'] if isinstance(x, dict) else x)
    df['Venue'] = df['Venue'].apply(lambda x: x['VenueName'] if isinstance(x, dict) else x)

    # Save to CSV
    df.to_csv("best_schedule.csv", index=False)

    visualize_schedule(sort_schedule(best_schedule))