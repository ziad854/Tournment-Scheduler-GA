import matplotlib.pyplot as plt
from matplotlib.table import Table
from matplotlib.patches import Rectangle
from datetime import datetime, timedelta
from collections import defaultdict

def visualize_schedule(schedule, constraints):
    """
    Visualize the tournament schedule with clear constraint violation highlighting.
    
    Args:
        schedule: List of matches in format (team1, team2, venue, day, time_slot, week)
        constraints: Dictionary containing constraints configuration
    """
    if not schedule:
        print("No matches to display!")
        return

    # Calculate all violations first
    venue_conflicts = count_venue_conflicts(schedule, constraints)
    rest_violations = count_rest_violations(schedule, constraints)
    time_imbalances = count_time_imbalances(schedule)

    # Prepare data with violation indicators
    headers = ["Week", "Day", "Time", "Venue", "Home", "Away", 
               "Venue Conflict", "Rest Violation", "Time Imbalance"]
    
    # Create violation trackers
    venue_violations = defaultdict(int)
    rest_violations_dict = defaultdict(int)
    time_slot_counts = defaultdict(lambda: defaultdict(int))
    
    # First pass to count time slots per team
    for match in schedule:
        team1, team2, _, _, time_slot, _ = match
        time_slot_counts[team1['TeamID']][time_slot] += 1
        time_slot_counts[team2['TeamID']][time_slot] += 1

    table_data = [headers]
    for match in schedule:
        team1, team2, venue, day, time_slot, week = match
        
        # Check venue conflict
        venue_key = (venue["VenueID"], day, week, time_slot)
        venue_violations[venue_key] += 1
        has_venue_conflict = venue_violations[venue_key] > 1
        
        # Check rest violation
        current_date = day_to_date(day, week)
        team1_last = constraints.get('team_last_played', {}).get(team1['TeamID'])
        team2_last = constraints.get('team_last_played', {}).get(team2['TeamID'])
        
        has_rest_violation = False
        if team1_last and (current_date - team1_last).days < constraints.get('min_rest_days', 3):
            has_rest_violation = True
        if team2_last and (current_date - team2_last).days < constraints.get('min_rest_days', 3):
            has_rest_violation = True
            
        # Check time imbalance (if team plays in same slot too often)
        team1_imbalance = time_slot_counts[team1['TeamID']][time_slot] > 2
        team2_imbalance = time_slot_counts[team2['TeamID']][time_slot] > 2
        has_time_imbalance = team1_imbalance or team2_imbalance

        table_data.append([
            week,
            day,
            time_slot,
            venue['VenueName'],
            team1['TeamName'],
            team2['TeamName'],
            "⚠️" if has_venue_conflict else "",
            "⚠️" if has_rest_violation else "",
            "⚠️" if has_time_imbalance else ""
        ])

    # Create figure
    fig, ax = plt.subplots(figsize=(16, max(8, len(table_data)*0.5)))
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
    
    # Color coding for violations
    for i in range(1, len(table_data)):
        # Venue conflict coloring
        if table_data[i][6] == "⚠️":
            table[(i, 6)].set_facecolor('#FF9999')  # Light red
        # Rest violation coloring
        if table_data[i][7] == "⚠️":
            table[(i, 7)].set_facecolor('#FFCC99')  # Light orange
        # Time imbalance coloring
        if table_data[i][8] == "⚠️":
            table[(i, 8)].set_facecolor('#FFFF99')  # Light yellow

    # Header styling
    for j in range(len(headers)):
        table[(0, j)].set_facecolor('#2E86C1')
        table[(0, j)].set_text_props(color='white', weight='bold')

    # Add summary annotation
    summary_text = (f"Total Venue Conflicts: {venue_conflicts} | "
                   f"Total Rest Violations: {rest_violations} | "
                   f"Time Imbalance Score: {time_imbalances}")
    plt.figtext(0.5, 0.01, summary_text, ha='center', fontsize=12)

    plt.tight_layout()
    plt.show()

# Helper functions (same as your original implementations)
def count_venue_conflicts(individual, constraints): ...
def count_rest_violations(individual, constraints): ...
def count_time_imbalances(individual): ...
def day_to_date(day, week): ...
