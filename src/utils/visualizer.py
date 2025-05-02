import matplotlib.pyplot as plt

def visualize_schedule(schedule):
    """
    Visualize the tournament schedule as a Gantt chart or table.
    """
    fig, ax = plt.subplots()
    for match in schedule.schedule:
        ax.broken_barh([(match.start_time, match.duration)], (match.venue, 1))
    plt.show()