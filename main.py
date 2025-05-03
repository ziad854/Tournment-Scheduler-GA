from src.ga.fitness import evaluate_fitness
from src.ga.scheduler import genetic_algorithm
from src.utils.parser import parse_input_data
from src.utils.visualizer import visualize_schedule
from src.utils.analsyis import analyze_schedule

if __name__ == "__main__":
    # Load input data
    data = parse_input_data("data/data.json")


    # Run GA
    final_population = genetic_algorithm(data , population_size=1000 )

    # Visualize best schedule
    best_schedule = max(final_population, key=lambda s: evaluate_fitness(s, data))

    all_played_all, no_simultaneous_matches = analyze_schedule(best_schedule)
    print(f"Every team plays every other team exactly once: {all_played_all}")
    print(f"No team plays multiple matches at the same time: {no_simultaneous_matches}")

    # number_of_teams = len(best_schedule['teams'])
    # print(f"Number of teams: {number_of_teams}")
    print(f"Best schedule fitness: {evaluate_fitness(best_schedule, data)}")

    visualize_schedule(best_schedule)