from src.ga.fitness import evaluate_fitness
from src.ga.scheduler import genetic_algorithm
from src.utils.parser import parse_input_data
from src.utils.visualizer import visualize_schedule
from src.utils.analsyis import analyze_schedule

if __name__ == "__main__":
    # Load input data
    constraints = parse_input_data(r"D:\FCAI-HU\Level 3\semester2\Projects\EA_Project\Tournment-Scheduler-GA\data\data.json")


    # Run GA
    best_population, best_fitness  = genetic_algorithm(constraints , population_size=2000 )

    # Visualize best schedule
    best_schedule = max(best_population, key=lambda s: evaluate_fitness(s, constraints))

    # all_played_all, no_simultaneous_matches = analyze_schedule(best_schedule)
    # print(f"Every team plays every other team exactly once: {all_played_all}")
    # print(f"No team plays multiple matches at the same time: {no_simultaneous_matches}")
    all_played_all, no_simultaneous_matches = analyze_schedule(best_schedule)
    print(f"\nSchedule Analysis:")
    print(f"- Every team plays every other team exactly once: {all_played_all}")
    print(f"- No team plays multiple matches at the same time: {no_simultaneous_matches}")
    print(f"- Overall fitness score: {evaluate_fitness(best_schedule, constraints)}")

    # number_of_teams = len(best_schedule['teams'])
    # print(f"Number of teams: {number_of_teams}")
    print(f"Best schedule fitness: {evaluate_fitness(best_schedule, constraints)}")

    visualize_schedule(best_schedule,constraints)