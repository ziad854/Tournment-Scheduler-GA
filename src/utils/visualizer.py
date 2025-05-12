import matplotlib.pyplot as plt


def visualize_schedule(schedule, venue_violations_details, rest_violations_details, constraints):
    """
    Visualize the tournament schedule with clear constraint violation highlighting.

    Args:
        schedule: List of matches in format (team1, team2, venue, day, time_slot, week).
        venue_violations_details: Details about venue conflicts.
        rest_violations_details: Details about rest violations.
        constraints: Dictionary containing constraints configuration.
    """
    if not schedule:
        print("No matches to display!")
        return

    # Prepare headers for the table
    headers = ["Week", "Day", "Time", "Venue", "Home", "Away", 
               "Venue Conflict", "Rest Violation"]

    # Prepare table data
    table_data = [headers]
    for match in schedule:
        team1, team2, venue, day, time_slot, week = match

        # Check if the match has venue conflicts
        venue_key = (venue["VenueID"], day, week)
        venue_conflict = any(
            conflict["venue_key"] == venue_key for conflict in venue_violations_details
        )

        # Check if the match has rest period violations
        rest_violation = any(
            violation["team"] in [team1["TeamID"], team2["TeamID"]]
            for violation in rest_violations_details
        )

        table_data.append([
            week,
            day,
            time_slot,
            venue['VenueName'],
            team1['TeamName'],
            team2['TeamName'],
            "⚠️" if venue_conflict else "",
            "⚠️" if rest_violation else "",
        ])

    # Create the figure
    fig, ax = plt.subplots(figsize=(28, max(8, len(table_data)*0.5)))
    ax.axis('off')
    ax.set_title('Tournament Schedule with Constraint Violations', 
                fontsize=16, pad=20, weight='bold')

    # Create table
    table = ax.table(
        cellText=table_data,
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )

    # Styling
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Highlight violations
    for i in range(1, len(table_data)):
        # Highlight venue conflicts in light red
        if table_data[i][6] == "⚠️":
            table[(i, 6)].set_facecolor('#FF9999')  # Light red
        # Highlight rest violations in light orange
        if table_data[i][7] == "⚠️":
            table[(i, 7)].set_facecolor('#FFCC99')  # Light orange

    # Header styling
    for j in range(len(headers)):
        table[(0, j)].set_facecolor('#2E86C1')
        table[(0, j)].set_text_props(color='white', weight='bold')

    # # Generate violation summaries
    # violation_summary = generate_violation_summary(venue_violations_details, rest_violations_details)

    # # Adjust layout to make space for the violation summary below the table
    # plt.subplots_adjust(bottom=0.3)  # Increase bottom margin to make space

    # # Add the violation summary below the table
    # fig.text(
    #     0.5, 0.02,  # Position below the graph
    #     violation_summary,
    #     ha='center', fontsize=10, wrap=True
    # )

    plt.tight_layout()
    plt.show()

# def generate_violation_summary(venue_violations_details, rest_violations_details):
#     """
#     Generate a textual summary of the violations.

#     Args:
#         venue_violations_details: Details about venue conflicts.
#         rest_violations_details: Details about rest violations.

#     Returns:
#         A formatted string containing the summary of violations.
#     """
#     summary = f"Total Venue Conflicts: {len(venue_violations_details)}\n"
#     for conflict in venue_violations_details:
#         summary += (
#             f"- Venue Conflict at {conflict['venue_name']} on "
#             f"Week {conflict['week']}, Day {conflict['day']}, "
#             f"Time Slot {conflict['time_slot']}\n"
#         )

#     summary += f"\nTotal Rest Violations: {len(rest_violations_details)}\n"
#     for violation in rest_violations_details:
#         summary += (
#             f"- Rest Violation for Team {violation['team']} between "
#             f"Days {violation['match_days'][0]} and {violation['match_days'][1]} "
#             f"(Rest Period: {violation['rest_period']} days)\n"
#         )

#     return summary

