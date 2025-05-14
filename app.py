import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.ga.scheduler import genetic_algorithm
from src.ga.operators import *
from src.utils.helper import parse_input_data


# Configuration
st.set_page_config(layout="wide")
st.title("🏆 Tournament Scheduler using Genetic Algorithm")

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

pop_size = st.sidebar.slider("Population Size", 50, 2000, 500, step=50)
Gen_size = st.sidebar.slider("Generations Size", 50, 800, 200, step=50)

# Team input
st.header("1️⃣ Enter Teams")
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
st.header("2️⃣ Configure Genetic Algorithm")
mutation_method = st.selectbox("Select Mutation Method", ["swap_mutation", "attribute_level_mutation"])
crossover_method = st.selectbox("Select Crossover Method", ["PMX_Crossover", "order_crossover"])
survivor_strategy = st.selectbox("Select Survivor Strategy", ["elitism", "genitor"])

# Store selected methods in session state for use in the scheduler
if st.button("💾 Save Configuration"):
    st.session_state.mutation_method = mutation_method
    st.session_state.crossover_method = crossover_method
    st.session_state.survivor_strategy = survivor_strategy
    st.success(f"Configuration Saved: Mutation = {mutation_method}, Crossover = {crossover_method}, Survivor = {survivor_strategy}")

# Scheduler execution
st.header("3️⃣ Run Scheduler")
if st.button("🚀 Run Scheduler"):
    try:
        if st.session_state.mutation_method is None or st.session_state.crossover_method is None or st.session_state.survivor_strategy is None:
            st.error("Please configure the Genetic Algorithm (Step 2) before running the scheduler.")
        else:
            # Pass mutation and crossover methods to the genetic algorithm
            best_schedule, best_fitness, venue_violations, rest_period_violations, Generations_fitness = genetic_algorithm(
                constraints,
                population_size = pop_size,
                generations_size = Gen_size,
                mutation_method=st.session_state.mutation_method,
                crossover_method=st.session_state.crossover_method,
                survivor_strategy=st.session_state.survivor_strategy
            )

            st.session_state.schedule = best_schedule
            st.session_state.fitness_trend = best_fitness
            st.session_state.Generations_fitness = Generations_fitness
            st.session_state.constraints = constraints
    except Exception as e:
        st.error(f"Error: {e}")

# Display results
if st.session_state.schedule:
    schedule = st.session_state.schedule
    fitness_trend = st.session_state.fitness_trend
    Generations_fitness = st.session_state.Generations_fitness
    constraints = st.session_state.constraints

    # Fitness plot
    st.subheader("📈 Fitness Over Generations")
    fig, ax = plt.subplots()
    ax.plot(Generations_fitness, marker='o')
    ax.set_title("Fitness Progress")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Fitness")
    ax.grid(True)
    st.pyplot(fig)

    # Best Schedule
    st.subheader("🏆 Best Schedule")
    st.write("The best schedule found by the genetic algorithm is:")
    st.write("**Fitness Score:**", fitness_trend)
    

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

    st.dataframe(filtered_df.style.set_properties(**{
        'background-color': '#e8f4fc',
        'color': 'black',
        'border-color': 'gray'
    }))