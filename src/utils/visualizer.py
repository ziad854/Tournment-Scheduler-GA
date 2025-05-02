import matplotlib.pyplot as plt

def visualize_schedule(schedule):
    """
    Visualize the tournament schedule as a Gantt chart.
    :param schedule: A list of matches, where each match is a tuple
                     (team1, team2, venue_id, day, timeslot).
    """
    # Map days and timeslots to numeric values for visualization
    day_to_num = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }
    timeslot_to_offset = {
        "09:00-11:00": 0,
        "11:30-13:30": 1,
        "14:00-16:00": 2,
        "16:30-18:30": 3,
        "19:00-21:00": 4
    }

    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a broken bar chart for each match
    for match in schedule:
        team1, team2, venue_id, day, timeslot = match

        # Convert day and timeslot to numeric values
        day_num = day_to_num[day]
        timeslot_offset = timeslot_to_offset[timeslot]

        # Calculate the start and duration for the Gantt chart
        start_time = day_num * 24 + timeslot_offset * 2  # Each timeslot = 2 hours
        duration = 2

        # Add a bar for the match
        ax.broken_barh(
            [(start_time, duration)],
            (venue_id - 0.4, 0.8),  # Center the bar around the venue ID
            facecolors="tab:blue"
        )

        # Add labels for the teams
        ax.text(
            start_time + 0.5, venue_id,
            f"{team1} vs {team2}",
            va="center", ha="left", fontsize=8, color="black"
        )

    # Set labels and grid
    ax.set_xlabel("Time")
    ax.set_ylabel("Venue")
    ax.set_yticks(range(1, max(schedule, key=lambda x: x[2])[2] + 1))  # Venue IDs
    ax.set_xticks(range(0, 24 * 7, 2))  # Time in hours for the week
    ax.grid(True)

    # Show the plot
    plt.title("Tournament Schedule")
    plt.show()