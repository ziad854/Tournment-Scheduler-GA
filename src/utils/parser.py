import pandas as pd
import json

def parse_input_data(data_file):
    with open(data_file, "r") as f:
        constraints = json.load(f)
    return constraints