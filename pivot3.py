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

# Create a new 'level' column that merges lvl1, lvl2, lvl3
df['level'] = df[['lvl1', 'lvl2', 'lvl3']].apply(
    lambda x: next(y for y in x if y != '(blank)'), axis=1
)

# Pivot the table by summing 'Gross' and 'Net' based on 'level'
pivot_table = df.groupby('level')[['Gross', 'Net']].sum().reset_index()

# Sort so that (blank) rows appear first
pivot_table = pivot_table.sort_values(by='level', key=lambda col: col.str.startswith('(blank)'), ascending=False)

# Reset the index for a clean output
pivot_table.reset_index(drop=True, inplace=True)

print(pivot_table)