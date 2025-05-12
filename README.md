# 🏆 Tournament Scheduler using Genetic Algorithm

This is a Streamlit application and terminal-based tool for scheduling tournaments using a **Genetic Algorithm**. The application allows users to configure genetic algorithm parameters, upload constraints, and visualize the generated schedule. Additionally, the project includes a terminal-based runner for performing trials and experiments.

## 🚀 Features

- **Streamlit Web Application**: A user-friendly interface for configuring and running the genetic algorithm.
- **Terminal-Based Execution**: A `main.py` file for running simulations and trials directly from the terminal.
- **Upload Constraints**: Upload a JSON file containing tournament constraints.
- **Genetic Algorithm Configuration**: Choose mutation methods, crossover methods, and survivor strategies.
- **Fitness Tracking**: Visualize the fitness progress over generations.
- **Schedule Visualization**: View and filter the generated match schedule.
- **Interactive UI**: Fully interactive interface built with Streamlit.

---

## 🏗️ Installation

### Prerequisites
- Python 3.10 or higher
- [Streamlit](https://streamlit.io/)
- Required Python packages listed in [`requirements.txt`](#requirements)

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/ziad854/Tournment-Scheduler-GA.git
   cd Tournment-Scheduler-GA
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

4. Run the terminal-based tool:
   ```bash
   python main.py
   ```

5. Open the URL displayed in the terminal (e.g., `http://localhost:8501`) to access the web application.

---

## 📄 Usage

### 1️⃣ **Enter Teams**
- **In Streamlit**:
  - Select **Upload JSON File** to upload a constraints JSON file.
  - Alternatively, select **Run with Saved Data** to use preloaded constraints.
- **In Terminal**:
  - Use `main.py` to pass constraints directly in JSON format or use default saved data.

### 2️⃣ **Configure Genetic Algorithm**
- Choose the mutation method (e.g., `swap_mutation`, `attribute_level_mutation`).
- Choose the crossover method (e.g., `PMX_Crossover`, `order_crossover`).
- Choose the survivor strategy (e.g., `elitism`, `genitor`).

### 3️⃣ **Run the Scheduler**
- **In Streamlit**:
  - Click **Run Scheduler** to execute the genetic algorithm.
  - The algorithm generates the best schedule based on the provided constraints and configuration.
- **In Terminal**:
  - Run `main.py` with appropriate arguments to configure and execute the scheduler.

### 4️⃣ **View Results**
- **Fitness Over Generations**: View a plot of fitness progress in Streamlit.
- **Best Schedule**: See the best schedule and its fitness score.
- **Match Schedule**: Visualize the schedule in a table (Streamlit) or as terminal logs.

---

## 📦 File Structure

```
.
├── app.py                  # Main Streamlit application
├── main.py                 # Terminal-based tool for running the scheduler
├── data
│   └── data.json           # Example constraints file
├── src
│   ├── ga
│   │   ├── scheduler.py    # Genetic algorithm implementation
│   │   ├── operators.py    # Genetic operators (mutation, crossover)
│   │   ├── fitness.py      # Fitness evaluation functions
│   │   ├── population.py   # Population management functions
│   ├── utils
│   │   ├── helper.py       # Utility functions for data parsing
│   │   ├── grid_search.py  # Grid search for hyperparameter tuning
│   │   ├── visualizer.py   # Visualization utilities
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 📊 Constraints JSON Format

The constraints JSON file should include details about teams, venues, and scheduling rules. Example:

```json
{
  "teams": [
    {"TeamID": "1", "TeamName": "Team A"},
    {"TeamID": "2", "TeamName": "Team B"}
  ],
  "venues": [
    {"VenueID": "1", "VenueName": "Stadium A"},
    {"VenueID": "2", "VenueName": "Stadium B"}
  ],
  "rules": {
    "min_rest_days": 3,
    "max_games_per_week": 2
  }
}
```

---

## 🔧 Configuration Options

### Genetic Algorithm Settings
- **Population Size**: Number of individuals in each generation.
- **Generation Size**: Number of generations to run.
- **Mutation Methods**:
  - `swap_mutation`: Swaps two elements in the individual.
  - `attribute_level_mutation`: Alters an attribute of the individual.
- **Crossover Methods**:
  - `PMX_Crossover`: Partially Mapped Crossover.
  - `order_crossover`: Preserves the order of elements.
- **Survivor Strategies**:
  - `elitism`: Retains the best individuals from each generation.
  - `genitor`: Replaces the worst individuals.

---

## 📈 Output

### Fitness Progress
The fitness progress plot displays the best fitness score achieved across generations.

### Match Schedule
The generated schedule includes:
- Week, Day, and Time Slot.
- Venue, Home Team, and Away Team.
- Flags for violations (e.g., rest violations, venue conflicts).

---

## 🧪 Example Results

### Fitness Progress Plot
![Fitness Progress](path/to/fitness_progress_plot.png)

### Match Schedule Table
| Week | Day       | Time Slot    | Venue       | Team 1        | Team 2        |
|------|-----------|--------------|-------------|---------------|---------------|
| 1    | Monday    | 09:00-11:00 | Stadium A   | Team A        | Team B        |
| 1    | Tuesday   | 11:30-13:30 | Stadium B   | Team C        | Team D        |

---




## 🛠️ Requirements

- Python 3.10 or higher
- Required dependencies:
  ```plaintext
  pandas
  matplotlib
  streamlit
  ```

