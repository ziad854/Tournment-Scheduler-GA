import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import random
random.seed(42)  # For reproducibility

from src.ga.scheduler import genetic_algorithm
from src.ga.operators import *
from src.utils.helper import parse_input_data


# Configuration
st.set_page_config(layout="wide")
st.title("Tournament Scheduler using Genetic Algorithm")

# Session states
if 'schedule' not in st.session_state:
    st.session_state.schedule = None
if 'fitness_trend' not in st.session_state:
    st.session_state.fitness_trend = None
if 'constraints' not in st.session_state:
    st.session_state.constraints = None
if 'mutation_method' not in st.session_state:
    st.session_state.mutation_method = None
if 'crossover_method' not in st.session_state:
    st.session_state.crossover_method = None

# Sidebar configuration
st.sidebar.header("⚙️ Settings")

pop_size = st.sidebar.slider("Population Size", 100, 2000, 500, step=50)
Gen_size = st.sidebar.slider("Generations Size", 100, 800, 200, step=50)

# Team input
st.header("Enter Teams")
input_method = st.radio("Choose input method:", ["Upload JSON File", "Run with Saved Data"])
teams = []

if input_method == "Run with Saved Data":
    with open("data/data.json", "r") as f:
        constraints = parse_input_data(f)

if input_method == "Upload JSON File":
    uploaded_file = st.file_uploader("Upload JSON with constraints", type=["json"])
    if uploaded_file:
        constraints = parse_input_data(uploaded_file)

# Genetic Algorithm Configuration Step
st.header("Configure Genetic Algorithm")
mutation_method = st.selectbox("Select Mutation Method", ["swap_mutation", "attribute_level_mutation"])
crossover_method = st.selectbox("Select Crossover Method", ["PMX_Crossover", "order_crossover"])
survivor_strategy = st.selectbox("Select Survivor Strategy", ["elitism", "genitor"])
selection_method = st.selectbox("Select Selection Method", ["tournament_selection", "rank_based_selection"])

# Store selected methods in session state for use in the scheduler
if st.button("Save Configuration"):
    st.session_state.mutation_method = mutation_method
    st.session_state.crossover_method = crossover_method
    st.session_state.survivor_strategy = survivor_strategy
    st.session_state.selection_method = selection_method
    st.success(f"Configuration Saved: Mutation = {mutation_method}, Crossover = {crossover_method}, Survivor = {survivor_strategy}, Selection = {selection_method}")

# Scheduler execution
st.header("Run Scheduler")
if st.button(" Run Scheduler"):
    try:
        if st.session_state.mutation_method is None or st.session_state.crossover_method is None or st.session_state.survivor_strategy is None:
            st.error("Please configure the Genetic Algorithm (Step 2) before running the scheduler.")
        else:
            # Pass mutation and crossover methods to the genetic algorithm
            best_schedule, best_fitness, venue_violations, rest_period_violations, time_violations, Generations_fitness = genetic_algorithm(
                constraints,
                population_size = pop_size,
                generations_size = Gen_size,
                mutation_method=st.session_state.mutation_method,
                crossover_method=st.session_state.crossover_method,
                survivor_strategy=st.session_state.survivor_strategy,
                selection_method=st.session_state.selection_method
            )

            st.session_state.schedule = best_schedule
            st.session_state.fitness_trend = best_fitness
            st.session_state.Generations_fitness = Generations_fitness
            st.session_state.venue_violations = venue_violations
            st.session_state.rest_period_violations = rest_period_violations
            st.session_state.time_violations = time_violations
            st.session_state.constraints = constraints
    except Exception as e:
        st.error(f"Error: {e}")

# Display results
if st.session_state.schedule:
    schedule = st.session_state.schedule
    fitness_trend = st.session_state.fitness_trend
    Generations_fitness = st.session_state.Generations_fitness
    venue_violations = st.session_state.venue_violations
    rest_period_violations = st.session_state.rest_period_violations
    time_violations = st.session_state.time_violations
    constraints = st.session_state.constraints

    # Replace your current fitness plot code with this:
    st.subheader("📈 Fitness Over Generations")

    fig = px.line(
        x=list(range(len(Generations_fitness))), 
        y=Generations_fitness,
        markers=True,
        labels={"x": "Generation", "y": "Best Fitness"},
        title="Fitness Progress Over Generations",
        template="plotly_dark",
    )

    fig.update_layout(
        xaxis_title="Generation",
        yaxis_title="Best Fitness",
        hovermode="x unified",
        font=dict(size=14),
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    fig.update_traces(
        hovertemplate="<b>Generation:</b> %{x}<br><b>Fitness:</b> %{y:.4f}<extra></extra>",
        line=dict(width=2),
        marker=dict(size=8)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Best Schedule")
    st.write("The best schedule found by the genetic algorithm is:")
    st.write("**Fitness Score:**", fitness_trend)

    st.write("**Venue Violations:**")
    for venue, count in venue_violations.items():
        st.write(f"- {venue[0]}, week {venue[1]}, Days {venue[2]}: {count} violations")

    st.write("**Rest Period Violations:**")
    for violation in rest_period_violations:
        team, match_day, rest_period = violation.items()
        st.write(f"- {team[1]}, Days: {match_day[1]} (Rest Period: {rest_period[1]})")

    st.write("**Time Violations:**")
    for violation in time_violations:
        team, time_slot, count = violation.items()
        st.write(f"- {team[0]}, time slot: {time_slot[1]} (Count: {count[1]})")

    

    # Visual schedule table
    st.subheader("📅 Match Schedule")
    df_schedule = pd.DataFrame([
        {
            "Week": match[5],
            "Day": match[3],
            "Time Slot": match[4],
            "Venue": match[2]['VenueName'],
            "Team 1": match[0]['TeamName'],
            "Team 2": match[1]['TeamName']
        }
        for match in schedule
    ])
    df_schedule.sort_values(by=["Week", "Day", "Time Slot"], inplace=True)


    # Filters
    st.markdown("### 🔍 Filter Matches")
    filter_team = st.selectbox("Filter by Team", ["All"] + sorted(set(df_schedule["Team 1"]).union(df_schedule["Team 2"])))
    filter_venue = st.selectbox("Filter by Venue", ["All"] + sorted(df_schedule["Venue"].unique()))
    filter_day = st.selectbox("Filter by Day", ["All"] + sorted(df_schedule["Day"].unique()))
    filter_week = st.selectbox("Filter by Week", ["All"] + sorted(df_schedule["Week"].unique()))


    filtered_df = df_schedule
    if filter_team != "All":
        filtered_df = filtered_df[(filtered_df["Team 1"] == filter_team) | (filtered_df["Team 2"] == filter_team)]
    if filter_venue != "All":
        filtered_df = filtered_df[filtered_df["Venue"] == filter_venue]
    if filter_day != "All":
        filtered_df = filtered_df[filtered_df["Day"] == filter_day]
    if filter_week != "All":
        filtered_df = filtered_df[filtered_df["Week"] == filter_week]

    csv = df_schedule.to_csv(index=False)
    st.download_button(label="Download Schedule as CSV", data=csv, file_name='data/schedule.csv', mime='text/csv')

    

    st.dataframe(filtered_df.style.set_properties(**{
        'background-color': '#e8f4fc',
        'color': 'black',
        'border-color': 'gray'
    }))