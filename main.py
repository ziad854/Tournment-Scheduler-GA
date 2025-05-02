from src.ga.fitness import evaluate_fitness
from src.ga.scheduler import genetic_algorithm
from src.utils.parser import parse_input_data
from src.utils.visualizer import visualize_schedule

if __name__ == "__main__":
    # Load input data
    teams, venues, constraints = parse_input_data("data/teams.csv", "data/venues.csv", "data/constraints.json")

    # Run GA
    final_population = genetic_algorithm(teams, venues, constraints)

    # Visualize best schedule
    best_schedule = max(final_population, key=lambda s: evaluate_fitness(s.schedule, constraints))
    visualize_schedule(best_schedule)