import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.ga.scheduler import genetic_algorithm  
from src.utils.parser import parse_input_data
from src.utils.visualizer import visualize_schedule

# Initial config
st.set_page_config(layout="wide")
st.title("⚽ Match Scheduler using Genetic Algorithm")

# Sidebar
st.sidebar.header("⚙️ Configuration")
pop_size = st.sidebar.slider("Population Size", 10, 200, 50, step=10)
generations = st.sidebar.slider("Number of Generations", 10, 500, 100, step=10)

# Input Data
data = parse_input_data("data/data.json")

# Run algorithm
if st.button("🚀 Run Genetic Algorithm"):
    with st.spinner("Running optimization..."):
        best_schedule = genetic_algorithm(data, population_size=pop_size )
        st.session_state.schedule_result = best_schedule

    st.success("✅ Optimization complete!")

# Display results if available
if 'schedule_result' in st.session_state and st.session_state.schedule_result:
    best_schedule = st.session_state.schedule_result


    # Display fitness trend

    # Display best match schedule
    st.subheader("📅 Final Match Schedule")
    visualize_schedule(best_schedule)

else:
    st.info("Click the button above to run the Genetic Algorithm and display results.")