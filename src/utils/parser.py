import pandas as pd
import json

def parse_input_data(data_file):
    try:
        with open(data_file, "r") as f:
            constraints = json.load(f)
        return constraints
    except Exception as e:
        raise RuntimeError(f"An error occurred while parsing the file {data_file}: {e}")