import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.ga.fitness import evaluate_fitness
from src.ga.scheduler import genetic_algorithm
from src.utils.parser import parse_input_data
from src.utils.analsyis import analyze_schedule

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

# Sidebar configuration
st.sidebar.header("⚙️ Settings")
pop_size = st.sidebar.slider("Population Size", 100, 5000, 2000, step=100)

# Team input
st.header("1️⃣ Enter Teams")
input_method = st.radio("Choose input method:", ["Upload JSON File", "Run with Saved Data"])
teams = []

if input_method == "Run with Saved Data":
    constraints = parse_input_data("data/data.json")

        
if input_method == "Upload json File":
    uploaded_file = st.file_uploader("Upload Json with constrains", type=["Json"])
    if uploaded_file:
        constraints = parse_input_data(uploaded_file)        

# Run algorithm
st.header("1️⃣ Load Json file containing data & Run GA")
if st.button("🚀 Run Scheduler"):
    try:
        # constraints['teams'] = teams
        best_schedule, fitness_trend = genetic_algorithm(constraints, population_size=100, genrations_size=100)
        # best_schedule = max(best_population, key=lambda s: evaluate_fitness(s, constraints))

        st.session_state.schedule = best_schedule
        st.session_state.fitness_trend = fitness_trend
        st.session_state.constraints = constraints

        # all_played_all, no_simultaneous = analyze_schedule(best_schedule)
        # st.success(f"Fitness: {evaluate_fitness(best_schedule, constraints):.4f}")
        # st.info(f"All teams play every other team once: {'✅' if all_played_all else '❌'}")
        # st.info(f"No simultaneous matches for same team: {'✅' if no_simultaneous else '❌'}")
    except Exception as e:
            st.error(f"Error: {e}")

# Display results
if st.session_state.schedule:
    schedule = st.session_state.schedule
    fitness_trend = st.session_state.fitness_trend
    constraints = st.session_state.constraints

    # Fitness plot
    st.subheader("📈 Fitness Over Generations")
    fig, ax = plt.subplots()
    ax.plot(fitness_trend, marker='o')
    ax.set_title("Fitness Progress")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Fitness")
    ax.grid(True)
    st.pyplot(fig)

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

    filtered_df = df_schedule
    if filter_team != "All":
        filtered_df = filtered_df[(filtered_df["Team 1"] == filter_team) | (filtered_df["Team 2"] == filter_team)]
    if filter_venue != "All":
        filtered_df = filtered_df[filtered_df["Venue"] == filter_venue]
    if filter_day != "All":
        filtered_df = filtered_df[filtered_df["Day"] == filter_day]

    st.dataframe(filtered_df.style.set_properties(**{
        'background-color': '#e8f4fc',
        'color': 'black',
        'border-color': 'gray'
    }))
