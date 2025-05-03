import matplotlib.pyplot as plt
from matplotlib.table import Table

# def visualize_schedule(schedule):
#     """
#     Visualize the tournament schedule as a table.

#     :param schedule: A list of matches where each match is a tuple in the format:
#                      (team1, team2, venue, day, time_slot, week)
#                      Example:
#                      [({'TeamID': 1, 'TeamName': 'Team Alpha'}, {'TeamID': 4, 'TeamName': 'Team Delta'},
#                       {'VenueID': 3, 'VenueName': 'Stadium C'}, 'Monday', '09:00-11:00', '1'), ...]
#     """
#     # Prepare data for the table
#     table_data = [["Week", "Day", "Time Slot", "Venue", "Team 1", "Team 2"]]
#     for match in schedule:
#         team1, team2, venue, day, time_slot, week = match
#         table_data.append([
#             week,
#             day,
#             time_slot,
#             venue['VenueName'],
#             team1['TeamName'],
#             team2['TeamName']
#         ])

#     # Create the plot for the table
#     fig, ax = plt.subplots(figsize=(12, len(table_data) * 0.5))
#     ax.axis('off')  # Turn off the axes

#     # Add the table
#     table = Table(ax, bbox=[0, 0, 1, 1])
#     n_rows, n_cols = len(table_data), len(table_data[0])
#     width, height = 1.0 / n_cols, 1.0 / n_rows

#     # Add cells
#     for i, row in enumerate(table_data):
#         for j, cell_text in enumerate(row):
#             table.add_cell(i, j, width, height, text=cell_text, loc='center', facecolor='white')

#     # Add header row with a different background color
#     for j, cell_text in enumerate(table_data[0]):
#         table.add_cell(0, j, width, height, text=cell_text, loc='center', facecolor='lightgrey')

#     # Add the table to the axis
#     ax.add_table(table)

#     # Show the table
#     plt.title("Tournament Schedule", fontsize=16, pad=20)
#     plt.show()



import matplotlib.pyplot as plt
from matplotlib.table import Table

def visualize_schedule(schedule):
    """
    Visualize the tournament schedule as a table.

    :param schedule: A list of matches where each match is a tuple in the format:
                     (team1, team2, venue, day, time_slot, week)
                     Example:
                     [({'TeamID': 1, 'TeamName': 'Team Alpha'}, {'TeamID': 4, 'TeamName': 'Team Delta'},
                      {'VenueID': 3, 'VenueName': 'Stadium C'}, 'Monday', '09:00-11:00', '1'), ...]
    """
    # Prepare data for the table
    table_data = [["Week", "Day", "Time Slot", "Venue", "Team 1", "Team 2"]]
    for match in schedule:
        team1, team2, venue, day, time_slot, week = match
        table_data.append([
            week,
            day,
            time_slot,
            venue['VenueName'],
            team1['TeamName'],
            team2['TeamName']
        ])

    # Create the plot for the table
    fig, ax = plt.subplots(figsize=(12, len(table_data) * 0.5))
    ax.axis('off')  # Turn off the axes

    # Add the table
    table = Table(ax, bbox=[0, 0, 1, 1])
    n_rows, n_cols = len(table_data), len(table_data[0])
    width, height = 1.0 / n_cols, 1.0 / n_rows

    # Add cells
    for i, row in enumerate(table_data):
        for j, cell_text in enumerate(row):
            table.add_cell(i, j, width, height, text=cell_text, loc='center', facecolor='white')

    # Add header row with a different background color
    for j, cell_text in enumerate(table_data[0]):
        table.add_cell(0, j, width, height, text=cell_text, loc='center', facecolor='lightgrey')

    # Add the table to the axis
    ax.add_table(table)

    # Show the table
    plt.title("Tournament Schedule", fontsize=16, pad=20)
    plt.show()