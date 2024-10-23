# config = [['x', 'y'], ['a', 'b']]

# for i, (item_a, item_b) in enumerate(config):
#     print(f'Index {i}: item a: {item_a}, item b: {item_b}')

import pandas as pd
import json

# Flatten nested JSON
data = '''
[
  {"id": 1, "name": "Alice", "info": {"age": 25, "city": "New York"}},
  {"id": 2, "name": "Bob", "info": {"age": 30, "city": "San Francisco"}}
]
'''

# Step 1: Parse the JSON string into a Python object (list of dictionaries)
data_parsed = json.loads(data)

# Step 2: Use pd.json_normalize to flatten the nested structure
df = pd.json_normalize(data_parsed)

# Step 3: Print the DataFrame
print(df)