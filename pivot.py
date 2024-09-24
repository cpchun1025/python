import pandas as pd

# Data as a list of lists
data = [
    ['A', '', '', 10, 10],
    ['A', 'B', '', 10, 10],
    ['A', 'B', 'B1', 20, 20],
    ['A', 'B', 'B1', 30, 30],
    ['A', 'B', '', 40, 40],
    ['A', 'C', '', 50, 50],
    ['A', 'C', '', 60, 60],
    ['A', 'D', '', 70, 70]
]

# Create a DataFrame
df = pd.DataFrame(data, columns=['lvl1', 'lvl2', 'lvl3', 'Gross', 'Net'])

# Replace empty strings with '(blank)'
df.fillna('(blank)', inplace=True)
df.replace('', '(blank)', inplace=True)

# Create a new 'level' column that consolidates lvl1, lvl2, and lvl3
rows = []
for index, row in df.iterrows():
    if row['lvl3'] != '(blank)':
        rows.append([row['lvl3'], row['Gross'], row['Net']])
    elif row['lvl2'] != '(blank)':
        rows.append([row['lvl2'], row['Gross'], row['Net']])
        rows.append(['(blank)', row['Gross'], row['Net']])
    else:
        rows.append([row['lvl1'], row['Gross'], row['Net']])
        rows.append(['(blank)', row['Gross'], row['Net']])

# Create a new DataFrame from the rows
df_pivoted = pd.DataFrame(rows, columns=['Row Labels', 'Gross', 'Net'])

# Pivot the table by summing 'Gross' and 'Net'
pivot_table = df_pivoted.groupby(['Row Labels']).sum().reset_index()

# Sort the pivot table in the order:
# non-blank values first, then (blank) for each level
sorted_table = pd.concat([
    pivot_table[pivot_table['Row Labels'] != '(blank)'],
    pivot_table[pivot_table['Row Labels'] == '(blank)']
], ignore_index=True)

# Print the final table
print(sorted_table)