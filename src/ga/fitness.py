from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd




def count_venue_conflicts(df, constraints):
    """
    Count venue conflicts based on the schedule.

    :param individual: The schedule to evaluate, where each match contains:
                       (team1, team2, venue, day, timeslot, week).
    :param constraints: The constraints dictionary (not used in this implementation but can be extended).
    :return: The number of venue conflicts and detailed conflict information.
    """
    # Convert the schedule to a DataFrame for easier manipulation
    # schedule_data = [
    #     {
    #         "Team1": match[0]["TeamID"],
    #         "Team2": match[1]["TeamID"],
    #         "Venue": match[2]["VenueID"],
    #         "Day": match[3],
    #         "Timeslot": match[4],
    #         "Week": match[5]
    #     }
    #     for match in individual
    # ]
    # df = pd.DataFrame(schedule_data)

    # Combine Venue, Week, and Day into a single column
    df['VenueKey'] = df.apply(lambda row: (row['Venue'], row['Week'], row['Day']), axis=1)

    # Count occurrences of each (Venue, Week, Day)
    venue_usage_counts = df['VenueKey'].value_counts()

    # Identify conflicts (more than one match scheduled for the same (Venue, Week, Day))
    venue_violations = venue_usage_counts[venue_usage_counts > 1]

    # Total conflicts (subtract 1 for each over-scheduled venue)
    total_venue_violations = sum(venue_violations - 1)

    # Detailed conflict information
    violation_details = venue_violations.reset_index()
    violation_details.columns = ['(Venue, Week, Day)', 'MatchesScheduled']



    return total_venue_violations





from datetime import datetime, timedelta




import pandas as pd

def count_rest_violations(df, constraints):
    """
    Count rest period violations for teams using a pandas-based approach.

    :param schedule: The schedule to evaluate, where each match is a tuple:
                     (team1, team2, venue, day, timeslot, week).
    :param constraints: The constraints dictionary.
    :return: The total number of rest period violations.
    """
    # Minimum rest period in days (default to 3 days if not specified)
    min_rest_days = constraints.get("rest_periods", {}).get("minimum_hours", 72) // 24

    # Day name to index
    day_to_index = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2,
        "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
    }

    # schedule_data = [
    #     {
    #         "Team1": match[0]["TeamID"],
    #         "Team2": match[1]["TeamID"],
    #         "Venue": match[2]["VenueID"],
    #         "Day": match[3],
    #         "Timeslot": match[4],
    #         "Week": int(match[5]) 
    #     }
    #     for match in schedule
    # ]
    # df = pd.DataFrame(schedule_data)

    df_team1 = df[['Week', 'Day', 'Team1']].rename(columns={'Team1': 'Team'})
    df_team2 = df[['Week', 'Day', 'Team2']].rename(columns={'Team2': 'Team'})
    df_all = pd.concat([df_team1, df_team2])

    # Convert Week to int
    df_all['Week'] = df_all['Week'].astype(int)

    # Add DayIndex and AbsoluteDay
    df_all['DayIndex'] = df_all['Day'].map(day_to_index)
    df_all['AbsoluteDay'] = df_all['Week'] * 7 + df_all['DayIndex']


    # df_all['DayIndex'] = df_all['Day'].map(day_to_index)
    # df_all['AbsoluteDay'] = df_all['Week'] * 7 + df_all['DayIndex']


    total_violations = 0
    for team, group in df_all.groupby('Team'):
        sorted_days = sorted(group['AbsoluteDay'].tolist())
        for i in range(1, len(sorted_days)):
            if sorted_days[i] - sorted_days[i - 1] < 3:
                total_violations += 1

    return total_violations




def count_time_imbalances(schedule, constraints=None):
    """
    Count time imbalances where a team is scheduled to play more than once
    on the same day (same week and day) using a pandas-based approach.
    
    :param schedule: The schedule to evaluate, where each match is a tuple:
                     (team1, team2, venue, day, timeslot, week).
    :param constraints: The constraints dictionary (not used in this implementation but can be extended).
    :return: The total number of time imbalances (day-level scheduling conflicts).
    """
    # Step 1: Convert the schedule to a DataFrame
    schedule_data = [
        {
            "Team1": match[0]["TeamID"],
            "Team2": match[1]["TeamID"],
            "Day": match[3],
            "Week": int(match[5])  # Ensure week is an integer
        }
        for match in schedule
    ]
    df = pd.DataFrame(schedule_data)

    # Step 2: Create a unified list of matches for each team
    df_team1 = df[['Week', 'Day', 'Team1']].rename(columns={'Team1': 'Team'})
    df_team2 = df[['Week', 'Day', 'Team2']].rename(columns={'Team2': 'Team'})
    df_all = pd.concat([df_team1, df_team2])

    # Step 3: Count occurrences of each (week, day) for each team
    df_all['DailyKey'] = df_all.apply(lambda row: (row['Week'], row['Day']), axis=1)
    daily_counts = df_all.groupby(['Team', 'DailyKey']).size()

    # Step 4: Identify imbalances (where a team plays more than once on the same day)
    imbalances = daily_counts[daily_counts > 1]

    # Step 5: Calculate total imbalance score
    imbalance_score = sum(imbalances - 1)

    return imbalance_score


def evaluate_fitness(individual, constraints):
    """
    Fitness function to evaluate the quality of a schedule.
    :param schedule: The schedule to evaluate.
    :param constraints: Constraints to consider.
    :return: Fitness score (higher is better).
    """

    df = pd.DataFrame(individual, columns=["Team1", "Team2", "Venue", "Day", "Time Slot", "Week"])
    df['Team1'] = df['Team1'].apply(lambda x: x['TeamName'] if isinstance(x, dict) else x)
    df['Team2'] = df['Team2'].apply(lambda x: x['TeamName'] if isinstance(x, dict) else x)
    df['Venue'] = df['Venue'].apply(lambda x: x['VenueName'] if isinstance(x, dict) else x)
    score = 0

    # Example: Minimize venue conflicts
    score -= count_venue_conflicts(df, constraints)

    # Example: Ensure fair rest periods
    score -= count_rest_violations(df, constraints) 

    # Example: Balance game times
    # score -= count_time_imbalances(individual, constraints) 

    return score