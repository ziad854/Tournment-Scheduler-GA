import random
import matplotlib.pyplot as plt
from collections import defaultdict

# Fix random seed for reproducibility
random.seed(42)

# Teams and Venues
teams = ['Team A', 'Team B', 'Team C', 'Team D','Team Z', 'Team I','Team K','Team A']

venues = [
    "Santiago Bernabeu", "Camp Nou", "Wanda Metropolitano",
    "Ramon Sanchez Pizjuan", "Mestalla"
]

# Time Slots
time_slot_indices = list(range(21))  # 21 slots (7 days, 3 slots/day)
time_slot_display = {
    0: "Day 1, 15:00", 1: "Day 1, 18:00", 2: "Day 1, 21:00",
    3: "Day 2, 15:00", 4: "Day 2, 18:00", 5: "Day 2, 21:00",
    6: "Day 3, 15:00", 7: "Day 3, 18:00", 8: "Day 3, 21:00",
    9: "Day 4, 15:00", 10: "Day 4, 18:00", 11: "Day 4, 21:00",
    12: "Day 5, 15:00", 13: "Day 5, 18:00", 14: "Day 5, 21:00",
    15: "Day 6, 15:00", 16: "Day 6, 18:00", 17: "Day 6, 21:00",
    18: "Day 7, 15:00", 19: "Day 7, 18:00", 20: "Day 7, 21:00"
}

# 1. Create individual schedule
def create_individual(teams):
    matches = []
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):
            match = {
                'team1': teams[i],
                'team2': teams[j],
                'venue': random.choice(venues),
                'time_slot': random.choice(time_slot_indices)  # Numeric index
            }
            matches.append(match)
    return matches

# 2. Initialize population
def initialize_population(pop_size, teams):
    return [create_individual(teams) for _ in range(pop_size)]

# 3. Fitness Evaluation
def evaluate(individual):
    venue_conflicts = 0
    rest_violations = 0
    team_play_times = defaultdict(list)

    # Venue Conflict Check
    slot_venue = set()
    for match in individual:
        key = (match['venue'], match['time_slot'])
        if key in slot_venue:
            venue_conflicts += 1
        else:
            slot_venue.add(key)
        team_play_times[match['team1']].append(match['time_slot'])
        team_play_times[match['team2']].append(match['time_slot'])
        

    # Rest Period Violation Check
    for times in team_play_times.values():
        times.sort()
        for i in range(1, len(times)):
            if times[i] - times[i-1] < 2:  # At least 1 slot gap (~6-9 hours)
                rest_violations += 1

    # Total penalty
    total_penalty = (venue_conflicts * 10) + (rest_violations * 5)
    return -total_penalty

# 4. Tournament Selection
def tournament_selection(population, fitnesses, k=3):
    selected = random.sample(list(zip(population, fitnesses)), k) # we take a sample from population 
    selected.sort(key=lambda x: x[1], reverse=True) # sort by fitness and take the highest to be parent
    return selected[0][0]

# 5. Crossover (Order)
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[start:end] = parent1[start:end]

    p2_index = end
    c_index = end

    while None in child:
        gene = parent2[p2_index % size]
        if gene not in child:
            child[c_index % size] = gene
            c_index += 1
        p2_index += 1

    return child

# 6. Mutation
def mutate(individual):
    idx1, idx2 = random.sample(range(len(individual)), 2)
    individual[idx1]['time_slot'], individual[idx2]['time_slot'] = individual[idx2]['time_slot'], individual[idx1]['time_slot']
    individual[idx1]['venue'], individual[idx2]['venue'] = individual[idx2]['venue'], individual[idx1]['venue']

# 7. Main GA Loop
def genetic_algorithm(teams, pop_size=50, generations=100):
    population = initialize_population(pop_size, teams)
    best_fitness_progress = []
    best_fitness = float('-inf')
    stagnant_count = 0
    max_stagnant = 20

    for gen in range(generations):
        fitnesses = [evaluate(ind) for ind in population]
        current_best = max(fitnesses)
        if current_best <= best_fitness:
            stagnant_count += 1
            if stagnant_count >= max_stagnant:
                print(f"Stopping early at generation {gen} due to no improvement")
                break
        else:
            best_fitness = current_best
            stagnant_count = 0

        new_population = []
        for _ in range(pop_size):
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child = crossover(parent1, parent2)
            if random.random() < 0.2:
                mutate(child)
            new_population.append(child)

        population = new_population
        best_fitness_progress.append(current_best)

        if gen % 10 == 0 or gen == generations-1:
            print(f"Generation {gen} - Best Fitness: {current_best}")

    fitnesses = [evaluate(ind) for ind in population]
    best = population[fitnesses.index(max(fitnesses))]
    return best, best_fitness_progress

# 8. Plotting Fitness Progress
def plot_fitness(fitness_trend):
    plt.figure(figsize=(10,5))
    plt.plot(fitness_trend, marker='o')
    plt.title('Best Fitness Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.grid()
    plt.show()

# 9. Pretty Print Schedule
def print_schedule(schedule):
    headers = ["Team 1", "Team 2", "Venue", "Time Slot"]
    col_widths = [15, 15, 20, 12]  # Adjusted for shorter time format
    header_row = "│ " + " │ ".join(f"{header:<{width}}" for header, width in zip(headers, col_widths)) + " │"
    separator = "├" + "┬".join("─" * (width + 2) for width in col_widths) + "┤"
    top_border = "┌" + "┬".join("─" * (width + 2) for width in col_widths) + "┐"
    bottom_border = "└" + "┴".join("─" * (width + 2) for width in col_widths) + "┘"

    print("\nBest Schedule Found:")
    print(top_border)
    print(header_row)
    print(separator)

    for match in sorted(schedule, key=lambda x: x['time_slot']):
        time_slot = time_slot_display[match['time_slot']]
        row = [match['team1'], match['team2'], match['venue'], time_slot]
        print("│ " + " │ ".join(f"{item:<{width}}" for item, width in zip(row, col_widths)) + " │")

    print(bottom_border)

# Run the system
best_schedule, fitness_trend = genetic_algorithm(teams)
print_schedule(best_schedule)
plot_fitness(fitness_trend)